import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

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
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    for pokemon in pokemons:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
