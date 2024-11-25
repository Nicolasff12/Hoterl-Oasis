from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Task(models.Model):
  title = models.CharField(max_length=201)
  description = models.TextField(max_length=1001)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username


class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    checkin = models.DateField()
    checkout = models.DateField()
    estado = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)
    habitacion = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('doble', 'Doble'),
        ('suite', 'Suite'),
    ])
    adultos = models.PositiveIntegerField()  # Número de adultos
    menores = models.PositiveIntegerField()  # Número de niños

    def __str__(self):
        return f"{self.nombre} - {self.habitacion}"
    
    @property
    def total_huespedes(self):
        return self.adultos + self.menores  # Suma de adultos y niños

class Huespedes (models.Model):
    nombre=models.CharField(max_length=51)
    apellido=models.CharField(max_length=51)
    email=models.CharField(max_length=51)
    tipo_documento=models.CharField(max_length=2)
    numero_documento=models

class Personal (models.Model):
    nombre=models.CharField(max_length=51)
    apellido=models.CharField(max_length=51)
    email=models.CharField(max_length=51)
    contraseña=models.CharField(max_length=21)
    nombreHotel = models.ForeignKey('Hoteles' ,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f" personal: {self.nombre} - hotel: {self.nombreHotel.nombre}"

class Contact (models.Model):
    class OptionsContact(models.TextChoices):
        accommodation_quote = 'accommodation_quote', _('accommodation_quote')
        event_quote = 'event_quote', _('event_quote')
        lost_object = 'lost_object', _('lost_object')
        general_question = 'general_question', _('general_question')
        complaint = 'complaint', _('complaint')
        accommodation_reservation = 'accommodation_reservation', _('accommodation_reservation')
        event_reservation = 'event_reservation', _('event_reservation')
        special_request = 'special_request', _('special_request')

    name=models.CharField(max_length=200)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    subject=models.CharField(
        choices=OptionsContact.choices,
        default=OptionsContact.accommodation_quote,
    )
    message=models.CharField(max_length=500)
    

class Hoteles (models.Model):
    nombre=models.CharField(max_length=51)
    direccion=models.CharField(max_length=51)

    def __str__(self):
        return self.nombre


    
