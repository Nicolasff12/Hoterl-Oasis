from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username

class Huespedes (models.Model):
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    tipo_documento=models.CharField(max_length=2)
    numero_documento=models

class Personal (models.Model):
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    contraseña=models.CharField(max_length=20)
    nombreHotel = models.ForeignKey('Hoteles' ,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f" personal: {self.nombre} - hotel: {self.nombreHotel.nombre}"
    

class Hoteles (models.Model):
    nombre=models.CharField(max_length=50)
    direccion=models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
