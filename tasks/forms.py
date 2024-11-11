from django.forms import ModelForm
from .models import Task
from .models import Contact
from django import forms

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