from django.forms import ModelForm
from .models import Task
from django import forms
from .models import Reserva
from .models import Contact
from .models import Huespedes

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

class ContactForm(forms.Form):
    name =forms.CharField(label="name", max_length=100)
    email =forms.EmailField(label="email", max_length=100)
    phone =forms.CharField(label="phone", max_length=100)
    subject =forms.CharField(label="subject", max_length=100)
    message =forms.CharField(label="message", max_length=500)





class HuespedesForm(forms.ModelForm):
    class Meta:
        model = Huespedes
        fields = '__all__'  # o especifica los campos que necesitas




class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'nombre', 
            'identificacion', 
            'email', 
            'telefono', 
            'checkin', 
            'checkout', 
            'habitacion', 
            'adultos'
        ]

