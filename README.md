# TO-DO-LIST BACK

# Pasos a seguir para ejecutar el proyecto
## Clonar el repositorio
git clone https://github.com/diegovega007/task_management_back.git

## Acceder al repositorio
cd task_management_back

## Crear entorno virtual
pip install virtualenv virtualenvwrapper
mkvirtualenv djangovenv
workon djangovenv

## Instalar requerimientos del sistema
pip install -r requirements.txt

## Configurar base de datos en base a lo que se tiene el archivo settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_base_datos',
        'USER': 'postgres',
        'PASSWORD': 'contraseña_base_datos',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

## Realizar migraciones
python manage.py makemigrations
python manage.py migrate

## Correr proyecto
python manage.py runserver

## Acceder a la documentacion en swagger
http://127.0.0.1:8000/api

Nota: Para poder accesar a los ep se de Management se necesita hacer login con el mismo método que se
encuentra en la documentación, ese mismo le proporcionara un token que se introducira como acceso para 
las demas APis (se introduce en la opción que te da la aplicación dando clic en el boto "Authorize").

### Login con usuario admin
usuario: admin
contraseña: admin