# Generated by Django 3.1.14 on 2025-02-18 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_auto_20250218_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='defense',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Защита'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='health',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Здоровье'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='level',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='stamina',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Выносливость'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='strength',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Сила'),
        ),
    ]
