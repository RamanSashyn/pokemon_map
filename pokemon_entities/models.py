from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=False)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_jp = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True)
    previous_evolution = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_evolutions'
    )

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField("Appeared at", default=None)
    disappeared_at = models.DateTimeField("Disappeared at", default=None)

    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

def __str__(self):
        return f'{self.pokemon.title} {self.lat} {self.lon}'
