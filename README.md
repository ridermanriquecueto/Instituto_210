# Proyecto Gestión de Inscripciones a Final del **Instituto 210**

## Proyecto de articulación de materias de la Carrera Tecnicatura Superior en Analisís de Sistemas

## Instalación desde consola

Para descargar el proyecto se puede ejecutar:

`git clone git@gitlab.com:Naueru2/Instituto210.git`

Tambien se puede utilizar el siguiente codigo:

`https://gitlab.com/Naueru2/Instituto210.git`

Antes de iniciar el proyecto de deberá copiar el archivo:
Realizar esto dentro de la carpeta donde se clona el repositorio ejemplo : 


En Linux o desde Windows Powershell:
`cp settings_DEV.py settings.py`

En Windows CMD:
`copy settings_DEV.py settings.py`

Lo que se puede hacer manualmente es copiar la carpeta settings_DEV y pegarla en la misma carpeta pero con el nombre settings

Agregar 'inscripcionFinales', en INSTALLED_APPS dentro del archivo settings.py

Antes de realizar migraciones tienen que realizar el siguiente comando para ingresar a la rama principal:

`git checkout front`

Ahora con esto van a poder realizar todas las migraciones y pasos siguentes y tener la ultima version del proyecto

Posteriormente ejecutar las migrations faltantes:
C:\Users\usuario\Desktop\Instituto210-dev-back\Instituto210
#Recordar realizar estos comando en la carpeta que contenga el archivo manage.py

`python manage.py makemigrations`

`python manage.py migrate`

Si se presenta el siguiente error : no such tables : inscripcionFinales_usuario desde la consola deben poner el siguiente comando:

`manage.py migrate--run-syncdb`

Para acceder al backoffice http://127.0.0.1:8000/admin se deberá crear un usuario superadmin de la forma:

`python manage.py createsuperuser`

Para ejecutar el proyecto se debe:

`python manage.py runserver`

Para acceder al login, ingresar a http://127.0.0.1:8000 desde el navegador.

Para redireccionar al index luego del login agregar en settings.py

`LOGIN_REDIRECT_URL = 'inicio'`
<!-- Fin -->
"# Instituto210Proyecto"
#prueba prueba

En sistemas windows es necesario instalar el software GTK. El siguiente link los deriva al archivo .exe que se debe bajar : (https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe)