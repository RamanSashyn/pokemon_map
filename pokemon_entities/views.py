import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from django.templatetags.static import static
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()

    for pokemon in pokemons:
        for entity in pokemon['entities']:
            appear_time = entity.get('appeared_at')
            disappear_time = entity.get('disappeared_at')

            if appear_time and disappear_time:
                appear_time = localtime(appear_time)
                disappear_time = localtime(disappear_time)

                if appear_time <= current_time <= disappear_time:
                    add_pokemon(
                        folium_map, entity['lat'], entity['lon'], pokemon['img_url']
                    )

    active_pokemons = PokemonEntity.objects.filter(
        appeared_at__lte=current_time, disappeared_at__gte=current_time
    )

    for entity in active_pokemons:
        add_pokemon(
            folium_map, entity.lat, entity.lon,
            request.build_absolute_uri(entity.pokemon.photo.url) if entity.pokemon.photo else static(
                'default_pokemon.png')
        )

    pokemons_on_page = [
        {
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else static(
                'default_pokemon.png'),
            'title_ru': pokemon.title,
        }
        for pokemon in Pokemon.objects.all()
    ]

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    pokemon_info = {
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en or '',
        'title_jp': pokemon.title_jp or '',
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else static('default_pokemon.png'),
    }

    if pokemon.previous_evolution:
        pokemon_info['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(
                pokemon.previous_evolution.photo.url) if pokemon.previous_evolution.photo else static(
                'default_pokemon.png'),
        }

    next_evolution = Pokemon.objects.filter(previous_evolution=pokemon).first()

    if next_evolution:
        pokemon_info['next_evolution'] = {
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.photo.url) if next_evolution.photo else static(
                'default_pokemon.png'),
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    current_time = localtime()
    active_pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )

    for entity in active_pokemon_entities:
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            pokemon_info['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_info
    })
