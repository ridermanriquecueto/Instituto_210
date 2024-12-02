# Proyecto Gestión de Inscripciones a Final del Instituto 210

## Descripción
Este es un proyecto de articulación de materias de la Carrera Tecnicatura Superior en Análisis de Sistemas. Permite gestionar las inscripciones a finales en el Instituto 210.

## Instalación desde consola
Para descargar el proyecto, puedes ejecutar el siguiente comando:

```bash
git clone https://github.com/ridermanriquecueto/Instituto_210.git

Configuración del proyecto

Antes de iniciar el proyecto, debes copiar el archivo de configuración adecuado:
En Linux o desde Windows PowerShell:

cp settings_DEV.py settings.py

En Windows CMD:

copy settings_DEV.py settings.py

También puedes hacerlo manualmente: copia el archivo settings_DEV.py y pégalo en la misma carpeta con el nombre settings.py.
Configuración en Django

Agrega inscripcionFinales en el campo INSTALLED_APPS dentro del archivo settings.py.
Bajar la rama principal

Para ingresar a la rama principal, debes ejecutar el siguiente comando:

git checkout main

Con esto tendrás la última versión del proyecto.
Realizar las migraciones

Ejecuta las migraciones faltantes desde la carpeta que contiene el archivo manage.py:

python manage.py makemigrations
python manage.py migrate

Si se presenta el error no such table: inscripcionFinales_usuario, ejecuta:

python manage.py migrate --run-syncdb

Acceder al Backoffice

Para acceder al backoffice, abre la siguiente URL en tu navegador:

http://127.0.0.1:8000/admin

Debes crear un superusuario ejecutando:

python manage.py createsuperuser

Ejecutar el servidor

Para ejecutar el servidor, usa el siguiente comando:

python manage.py runserver

Redireccionamiento después del login

Para redirigir al index después de un login exitoso, agrega lo siguiente en el archivo settings.py:

LOGIN_REDIRECT_URL = 'inicio'

Instalación de GTK (solo en Windows)

Si estás utilizando Windows, es necesario instalar el software GTK. Puedes descargarlo desde el siguiente enlace:

GTK for Windows - Runtime Environment Installer


### **Cambios que hice en el archivo `README.md`:**

1. Actualicé los enlaces para que apunten a tu repositorio de **GitHub** en lugar de **GitLab**.
2. Cambié la referencia de la rama `front` a `main`, que es el nombre de la rama por defecto en GitHub (a menos que uses un nombre diferente).
3. Simplifiqué y estructuré un poco más la información para que sea clara y fácil de seguir.

De esta forma, tu `README.md` estará actualizado y tus reclutadores (o cualquier otra persona) podrán ver fácilmente los detalles del proyecto. ¡Hazme saber si necesitas más cambios o ayuda! 😊

Dijiste:
m podrias pswasr tdo eso en solo texto listo para copiar u pegar?
ChatGPT dijo:

Claro, aquí tienes el contenido del README.md listo para copiar y pegar:

# Proyecto Gestión de Inscripciones a Final del Instituto 210

## Descripción
Este es un proyecto de articulación de materias de la Carrera Tecnicatura Superior en Análisis de Sistemas. Permite gestionar las inscripciones a finales en el Instituto 210.

## Instalación desde consola
Para descargar el proyecto, puedes ejecutar el siguiente comando:

```bash
git clone https://github.com/ridermanriquecueto/Instituto_210.git

Configuración del proyecto

Antes de iniciar el proyecto, debes copiar el archivo de configuración adecuado:
En Linux o desde Windows PowerShell:

cp settings_DEV.py settings.py

En Windows CMD:

copy settings_DEV.py settings.py

También puedes hacerlo manualmente: copia el archivo settings_DEV.py y pégalo en la misma carpeta con el nombre settings.py.
Configuración en Django

Agrega inscripcionFinales en el campo INSTALLED_APPS dentro del archivo settings.py.
Bajar la rama principal

Para ingresar a la rama principal, debes ejecutar el siguiente comando:

git checkout main

Con esto tendrás la última versión del proyecto.
Realizar las migraciones

Ejecuta las migraciones faltantes desde la carpeta que contiene el archivo manage.py:

python manage.py makemigrations
python manage.py migrate

Si se presenta el error no such table: inscripcionFinales_usuario, ejecuta:

python manage.py migrate --run-syncdb

Acceder al Backoffice

Para acceder al backoffice, abre la siguiente URL en tu navegador:

http://127.0.0.1:8000/admin

Debes crear un superusuario ejecutando:

python manage.py createsuperuser

Ejecutar el servidor

Para ejecutar el servidor, usa el siguiente comando:

python manage.py runserver

Redireccionamiento después del login

Para redirigir al index después de un login exitoso, agrega lo siguiente en el archivo settings.py:

LOGIN_REDIRECT_URL = 'inicio'

Instalación de GTK (solo en Windows)

Si estás utilizando Windows, es necesario instalar el software GTK. Puedes descargarlo desde el siguiente enlace:

GTK for Windows - Runtime Environment Installer

