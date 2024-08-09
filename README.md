# Django Example Backend

Sistema construido con djangorestframework que permite a un usuario

    - Registrarse
    - Iniciar sesión
    - Salir de la sesión
    - Recuperar contraseña
    - Cambiar contraseña,
    - Actualizar perfil
    - Gestionar el registro de personas

## Pasos para crear el entorno de desarrollo

Cuando somos un usuario normal del sistema, en el terminal se mostrará el siguiente símbolo: ~$

Cuando accedemos al usuario root del sistema, en el terminal se mostrará el siguiente símbolo: ~#

Probado en últimas versiones estables de Debian y Ubuntu. Instalar los siguientes programas

    ~# apt install curl git graphviz graphviz-dev phppgadmin postgresql python3-dev virtualenv

Crear las siguientes carpetas

    ~$ mkdir Programación

Desde el terminal, moverse a la carpeta Programación y ejecutar

    ~$ cd Programación/

    ~$ mkdir python

Entrar a la carpeta python y hacer lo siguiente

    ~$ cd python/

    ~$ mkdir entornos_virtuales proyectos_django

Entrar a entornos_virtuales

    ~$ cd entornos_virtuales/

    ~$ mkdir django

Desde el terminal, moverse a la carpeta django y ejecutar

    ~$ cd django/

    ~$ virtualenv -p python3 django_example_backend

Para activar el entorno

    ~$ source django_example_backend/bin/activate

Nos movemos a la carpeta proyectos_django, descargamos el sistema y entramos a la carpeta con los siguientes comandos

    (django_example_backend) ~$ cd ../../proyectos_django/

    (django_example_backend) ~$ git clone https://github.com/willez88/django_example_backend.git

    (django_example_backend) ~$ cd django_example_backend/

    (django_example_backend) ~$ cp django_example_backend/settings.default.py django_example_backend/settings.py

    // Crear las siguientes carpetas
    (django_example_backend) ~$ mkdir db media

Tendremos las carpetas estructuradas de la siguiente manera

    // Entorno virtual
    Programación/python/entornos_virtuales/django/django_example_backend

    // Servidor de desarrollo
    Programación/python/proyectos_django/django_example_backend

Crear la base de datos para __django_example_backend__ usando PostgresSQL

    // Acceso al usuario postgres
    ~# su postgres

    // Acceso a la interfaz de comandos de PostgreSQL
    postgres@xxx:$ psql

    // Creación del usuario de a base de datos
    postgres=# CREATE USER admin WITH LOGIN ENCRYPTED PASSWORD '123' CREATEDB;
    postgres=# \q

    // Desautenticar el usuario PostgreSQL y regresar al usuario root
    postgres@xxx:$ exit

    // Salir del usuario root
    ~# exit

Puedes crear la base de datos colocando en el navegador: localhost/phppgadmin

    // Nombre de la base de datos: django_example_backend

Instalamos los requemientos que el sistema necesita en el entorno virtual

    (django_example_backend) ~$ pip install -r requirements/dev.txt

Hacer las migraciones

    (django_example_backend) ~$ python manage.py makemigrations base

    (django_example_backend) ~$ python manage.py migrate

    (django_example_backend) ~$ python manage.py loaddata auth_group 1_country 2_state 3_municipality 4_city 5_parish

Crear usuario administrador

    (django_example_backend) ~$ python manage.py createsuperuser

Correr el servidor de django

    (django_example_backend) ~$ python manage.py runserver

Poner en el navegador la url que sale en el terminal para entrar el sistema

Llegado hasta aquí el sistema ya debe estar funcionando

Para salir del entorno virtual se puede ejecutar desde cualquier lugar del terminal: deactivate

Generar gráfico del modelo Entidad-Relación

    // Grafica el modelo entidad-relación del proyecto
    (django_example_backend) ~$ python manage.py graph_models -a -g -o django_example_backend.svg

    // Grafica el modelo de una app del proyecto
    (django_example_backend) ~$ python manage.py graph_models base -g -o base.svg

Estilo de codificación PEP 8 en Visual Studio Code

    // Abre el proyecto con vscode
    (django_example_backend) ~$ code .

    Ir a extensiones del vscode e instalar
        ruff
        isort
        Python Environment Manager

    Python Environment Manager detectará todos los entornos virtuales creados
    en la sección Venv, click en "Set as active workspace interpreter" para activarlo

    Para que los cambios hagan efecto cerrar el vscode y abrirlo de nuevo

Exportar base de datos usando Django

    // Respaldo completo de los datos
    (django_example_backend) ~$ python manage.py dumpdata --indent 4 > db/django_example_backend.json

Importar base de datos usando Django

    // Resetear base de datos
    (django_example_backend) ~$ python manage.py reset_db

    // Eliminar las migraciones del proyecto
    (django_example_backend) ~$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

    // Eliminar los archivos compilados
    (django_example_backend) ~$ python manage.py clean_pyc

    // Ejecutar
    (django_example_backend) ~$ python manage.py makemigrations base
    
    (django_example_backend) ~$ python manage.py migrate

    // Luego entrar al gestor de base de datos
    //conectarse a la base de datos django_example_backend
    postgres=# \c django_example_backend

    // Vaciar las siguientes tablas para que no generen conflicto cuando se importen los datos
    django_example_backend=# TRUNCATE TABLE auth_permission CASCADE;
    django_example_backend=# TRUNCATE TABLE django_content_type CASCADE;

    // Por último importar django_example_backend.json
    (django_example_backend) ~$ python manage.py loaddata db/django_example_backend.json
