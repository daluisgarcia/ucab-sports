# Generated by Django 3.1.4 on 2021-01-21 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Juego',
                'verbose_name_plural': 'Juegos',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha del partido')),
                ('direccion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Partido',
                'verbose_name_plural': 'Partidos',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, verbose_name='Cédula')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('correo', models.EmailField(max_length=100, verbose_name='Email')),
                ('nickname', models.CharField(blank=True, max_length=30, verbose_name='Nickname')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='PrePerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, verbose_name='Cédula')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('correo', models.EmailField(max_length=100, verbose_name='Email')),
                ('nickname', models.CharField(blank=True, max_length=30, verbose_name='Nickname')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='PreTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/%Y/%m/%d')),
                ('comentario', models.CharField(blank=True, max_length=150, null=True, verbose_name='Comentario (opcional)')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Modalidad de Fase',
                'verbose_name_plural': 'Modalidades de Fase',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='team_logos')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de fin')),
                ('inscripcion_abierta', models.BooleanField(default=True)),
                ('edicion', models.SmallIntegerField(verbose_name='Edición')),
                ('tipo_delegado', models.CharField(choices=[('d', 'delegado'), ('jd', 'delegado y jugador')], default='d', max_length=2, verbose_name='Tipo de delegado')),
                ('id_juego', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.game', verbose_name='Tipo de juego')),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Torneo',
                'verbose_name_plural': 'Torneos',
            },
        ),
        migrations.CreateModel(
            name='StageTournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jerarquia', models.SmallIntegerField(verbose_name='Jerarquia')),
                ('participantes_por_equipo', models.SmallIntegerField(verbose_name='Participantes por equipo')),
                ('equipos_por_partido', models.SmallIntegerField(verbose_name='Equipos por partido')),
                ('num_grupos', models.SmallIntegerField(blank=True, null=True, verbose_name='Numero de grupos')),
                ('equipos_por_grupo', models.SmallIntegerField(blank=True, null=True, verbose_name='Equipos por grupo')),
                ('id_fase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.stage')),
                ('id_torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='PreTeamRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')),
                ('rol', models.CharField(choices=[('j', 'jugador'), ('d', 'delegado'), ('jd', 'delegado y jugador')], max_length=2, verbose_name='Rol')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.preteam')),
                ('id_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.preperson')),
                ('id_torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50, verbose_name='Título')),
                ('cuerpo', models.CharField(max_length=400, verbose_name='Contenido')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='')),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ganador', models.BooleanField(blank=True, null=True)),
                ('puntos_equipo', models.IntegerField(blank=True, null=True, verbose_name='Puntos del equipo')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team')),
                ('id_partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.match')),
            ],
            options={
                'verbose_name': 'Partido',
                'verbose_name_plural': 'Partidos',
            },
        ),
        migrations.AddField(
            model_name='match',
            name='id_fase_torneo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.stagetournament'),
        ),
        migrations.CreateModel(
            name='HistoryParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(verbose_name='Fecha de Registro')),
                ('fecha_fin', models.DateField(blank=True, null=True, verbose_name='Fecha de Registro')),
                ('rol', models.CharField(choices=[('j', 'jugador'), ('d', 'delegado'), ('jd', 'delegado y jugador')], max_length=2, verbose_name='Rol')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team')),
                ('id_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person')),
                ('id_torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='Classified',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(max_length=1, null=True, verbose_name='Grupo')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team')),
                ('id_fase_torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.stagetournament')),
            ],
        ),
    ]
