# Generated by Django 3.1.4 on 2021-01-07 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='equipos_por_grupo',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='num_grupos',
        ),
    ]
