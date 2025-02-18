from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name='Название покемона')
    title_en = models.CharField(max_length=200, blank=True, default='', verbose_name='Название покемона на английском')
    title_jp = models.CharField(max_length=200, blank=True, default='', verbose_name='Название покемона на японском')
    description = models.TextField(blank=True, verbose_name='Описание покемона')
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True, verbose_name='Фото покемона')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционирует'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Покемон'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name="Время появления", null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения", null=True, blank=True)

    level = models.PositiveIntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.PositiveIntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.PositiveIntegerField(null=True, blank=True, verbose_name='Сила')
    defense = models.PositiveIntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.PositiveIntegerField(null=True, blank=True, verbose_name='Выносливость')

def __str__(self):
        return f'{self.pokemon.title} {self.lat} {self.lon}'
