# Generated by Django 3.1.3 on 2020-12-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preteamregister',
            name='rol',
            field=models.CharField(choices=[('j', 'jugador'), ('d', 'delegado'), ('jd', 'delegado y jugador')], max_length=2, verbose_name='Rol'),
        ),
    ]
