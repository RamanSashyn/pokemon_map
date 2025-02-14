from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=False)
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField("Appeared at", default=None)
    disappeared_at = models.DateTimeField("Disappeared at", default=None)

    def __str__(self):
        return f'{self.pokemon.title} {self.lat} {self.lon}'
