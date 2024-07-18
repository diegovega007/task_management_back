from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.hashers import make_password

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

    def ready(self):
        from .models import User

        def create_user(sender, **kwargs):
            User.objects.get_or_create(
                username='admin',
                defaults={
                    'name': 'Admin',
                    'email': 'admin@gmail.com',
                    'password': make_password('admin')
                }
            )

        post_migrate.connect(create_user, sender=self)