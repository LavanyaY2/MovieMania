# Generated by Django 4.1.4 on 2023-08-24 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_movie_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='userId',
        ),
    ]