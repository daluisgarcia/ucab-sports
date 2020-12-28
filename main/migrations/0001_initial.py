# Generated by Django 3.1.3 on 2020-12-28 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=30, verbose_name='Usuario')),
                ('contrasena', models.CharField(max_length=30, verbose_name='Contraseña')),
            ],
            options={
                'verbose_name': 'Organizador',
                'verbose_name_plural': 'Organizadores',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Permiso',
                'verbose_name_plural': 'Permisos',
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
                ('equipos_por_grupo', models.SmallIntegerField(verbose_name='Equipos por grupo')),
                ('num_grupos', models.SmallIntegerField(verbose_name='Número de grupos')),
                ('part_por_equipo', models.SmallIntegerField(verbose_name='Participantes por equipo')),
                ('equipos_por_partido', models.SmallIntegerField(verbose_name='Equipos por partido')),
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
            name='WinningStandard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criterio', models.CharField(max_length=30, verbose_name='Criterio')),
            ],
            options={
                'verbose_name': 'Criterio Ganador',
                'verbose_name_plural': 'Criterios Ganadores',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de fin')),
                ('edicion', models.SmallIntegerField(verbose_name='Edición')),
                ('id_juego', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.game', verbose_name='Tipo de juego')),
                ('id_organizador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.organizer')),
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
                ('id_fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.stage')),
                ('id_torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='StageStandard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importancia', models.SmallIntegerField(verbose_name='Importancia')),
                ('id_crit_ganador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.winningstandard')),
                ('id_fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.stage')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('rol_permiso', models.ManyToManyField(to='main.Permission')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='PreTeamRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')),
                ('rol', models.CharField(choices=[('j', 'jugador'), ('d', 'delegado'), ('jd', 'delegado y jugador')], max_length=2, verbose_name='Rol')),
                ('estatus', models.CharField(max_length=1, verbose_name='Estatus')),
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
                ('id_organizador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.organizer')),
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
                ('ganador', models.BooleanField()),
                ('puntos_equipo', models.IntegerField(verbose_name='Puntos del equipo')),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team')),
                ('id_partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.match')),
            ],
            options={
                'verbose_name': 'Partido',
                'verbose_name_plural': 'Partidos',
            },
        ),
        migrations.AddField(
            model_name='organizer',
            name='id_rol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.role'),
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
    ]
