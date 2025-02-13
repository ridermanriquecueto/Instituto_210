# Generated by Django 5.1.2 on 2024-10-23 03:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=100, null=True, unique=True, verbose_name='username')),
                ('nombre_completo', models.CharField(blank=True, max_length=200, null=True, verbose_name='nombre_completo')),
                ('fecha_nac', models.DateField(blank=True, null=True, verbose_name='fecha_nac')),
                ('dni', models.IntegerField(blank=True, null=True, unique=True, verbose_name='dni')),
                ('direccion', models.CharField(blank=True, max_length=50, null=True, verbose_name='direccion')),
                ('localidad', models.CharField(blank=True, max_length=50, null=True, verbose_name='localidad')),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True, verbose_name='ciudad')),
                ('nacionalidad', models.CharField(blank=True, max_length=50, null=True, verbose_name='nacionalidad')),
                ('telefono_1', models.IntegerField(blank=True, null=True, verbose_name='telefono_1')),
                ('telefono_2', models.IntegerField(blank=True, null=True, verbose_name='telefono_2')),
                ('estado_civil', models.CharField(blank=True, choices=[('Casado/a', 'Casado/a'), ('Soltero/a', 'Soltero/a'), ('Viudo/a', 'Viudo/a'), ('Divorciado/a', 'Divorciado/a')], max_length=50, null=True, verbose_name='estado_civil')),
                ('sexo', models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], max_length=10, null=True, verbose_name='sexo')),
                ('imagen', models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='imagenPerfil')),
                ('is_admin', models.BooleanField(default=False, verbose_name='is_admin')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='is_superuser')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('rol', models.CharField(choices=[('Directivo', 'Directivo'), ('Preceptor', 'Preceptor'), ('Profesor', 'Profesor'), ('Estudiante', 'Estudiante'), ('Administrador', 'Administrador'), ('Bibliotecario', 'Bibliotecario')], default='Estudiante', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_carrera', models.CharField(max_length=100, unique=True, verbose_name='nombre_carrera')),
                ('num_resolucion', models.CharField(blank=True, max_length=100, null=True, verbose_name='num_resolucion')),
                ('duracion_carrera', models.PositiveBigIntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Instituto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_instituto', models.CharField(max_length=100, unique=True, verbose_name='nombre_instituto')),
                ('email_instituto', models.EmailField(max_length=254, unique=True, verbose_name='email_instituto')),
                ('direccion', models.CharField(max_length=50, verbose_name='direccion')),
                ('localidad', models.CharField(max_length=50, verbose_name='localidad')),
                ('ciudad', models.CharField(max_length=100, verbose_name='ciudad')),
                ('telefono_1', models.IntegerField(verbose_name='telefono_1')),
                ('telefono_2', models.IntegerField(verbose_name='telefono_2')),
                ('imagen', models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='imagenPerfil')),
            ],
        ),
        migrations.CreateModel(
            name='Directivo',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cargo', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('inscripcionFinales.usuario',),
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('matricula', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('inscripcionFinales.usuario',),
        ),
        migrations.CreateModel(
            name='Preceptor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('area', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('inscripcionFinales.usuario',),
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('especialidad', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('inscripcionFinales.usuario',),
        ),
        migrations.AddField(
            model_name='usuario',
            name='carrera',
            field=models.ManyToManyField(blank=True, to='inscripcionFinales.carrera'),
        ),
        migrations.AddField(
            model_name='carrera',
            name='instituto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inscripcionFinales.instituto'),
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_materia', models.CharField(max_length=50, verbose_name='nombre_materia')),
                ('inscripcionAbierta', models.BooleanField(default=False)),
                ('Horario', models.CharField(choices=[('12:00', '12:00'), ('14:00', '14:00'), ('16:00', '16:00'), ('18:00', '18:00'), ('20:00', '20:00')], default='12:00', max_length=22)),
                ('anio', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], default=1)),
                ('dia', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes')], default='Lunes', max_length=20)),
                ('carrera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inscripcionFinales.carrera')),
                ('profesor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='materia_carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inscripcionFinales.carrera')),
                ('materia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inscripcionFinales.materia')),
            ],
        ),
        migrations.CreateModel(
            name='MateriaCorrelativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias_correlativas', to='inscripcionFinales.materia')),
                ('materia_correlativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correlativas_de', to='inscripcionFinales.materia')),
            ],
        ),
        migrations.CreateModel(
            name='MesaFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('llamado', models.DateTimeField(verbose_name='Llamado')),
                ('vigente', models.BooleanField(default=True)),
                ('inscripcionAbierta', models.BooleanField(default=False)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscripcionFinales.materia')),
            ],
        ),
        migrations.CreateModel(
            name='InscripcionFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprobada', models.BooleanField(null=True)),
                ('inscripcionAbierta', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('llamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscripcionFinales.mesafinal')),
            ],
        ),
        migrations.CreateModel(
            name='usuarios_carreras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carreras', models.ManyToManyField(to='inscripcionFinales.carrera')),
                ('usuario', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='usuarios_materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota_cursada', models.FloatField(blank=True, null=True, verbose_name='Nota de Cursada')),
                ('nota_final', models.FloatField(blank=True, null=True, verbose_name='Nota de Final')),
                ('aprobada', models.BooleanField(default=False)),
                ('condicional', models.BooleanField(default=False)),
                ('modalidad', models.CharField(blank=True, choices=[('01', 'Regular'), ('02', 'Libre'), ('03', 'Condicional')], max_length=2, null=True, verbose_name='Modalidad')),
                ('ciclo_lectivo', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Ciclo lectivo')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscripcionFinales.materia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
