from django.contrib.auth.hashers import check_password
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }
    
    def validate_password(self, password):
        return check_password(password, self.password)