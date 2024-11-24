from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
from .models import Contact
from django.views.decorators.csrf import csrf_exempt

from .forms import TaskForm
from .forms import ContactForm
from django.shortcuts import render
from django.http import JsonResponse
import pytesseract
from PIL import Image
import io
import re

# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})



@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


def home(request):
    return render(request, 'home.html')

def check_in(request):
    return render(request, 'check_in.html')


def check_out(request):
    return render(request, 'check_out.html')


def tarjetaRegistro(request):
    return render(request, 'tarjetaRegistro.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
def reserva_form(request):
    return render(request, 'reserva_form.html')

def contacto(request):
    nav_2 = 'true'
    print(f"Request method: {request.method}")

    if request.method == 'GET':
        return render(request, 'contacto.html', {'nav_2': nav_2})

    elif request.method == 'POST':
        try:
            form = ContactForm(request.POST)
            data = request.POST

            print(data)
            if form.is_valid():
                new_contact = Contact(
                    name=data['name'],
                    email=data['email'],
                    phone=data['phone'],
                    subject=data['subject'],
                    message=data['message'],
                )
                
                new_contact.save()
            else:
                print(form.errors)  # This will print form validation errors to the console
                return render(request, 'contacto.html', {'form': form, 'error': 'Informacion erronea'})

            return redirect('hotel')

        except IntegrityError:
            # If there's an IntegrityError (e.g., duplicate username), render the form with an error message
            return render(request, 'signup.html', {"form": UserCreationForm(), "error": "Username already exists."})

    return render(request, 'contacto.html')  # Default render for the GET method if no other condition matches
    #     return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@csrf_exempt
def validar_ocr(request):
     return render(request, 'validar_ocr.html')
    
def hotel_view(request):
    return render(request, 'portal.html')

def principal(request):
    obj=Hoteles.objects.all().values("nombre")
    for i in obj:
        response_var+=f"{i}"
    return HttpResponse(response_var)

#CRUDE RESERVA 


from django.shortcuts import render, get_object_or_404, redirect
from .models import Huespedes
from .forms import HuespedesForm

# Crear un producto
def create_huesped(request):
    form = HuespedesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('huesped_list')
    return render(request, 'myapp/huesped_form.html', {'form': form})

# Leer (listar) los huéspedes
def huesped_list(request):
    huespedes = Huespedes.objects.all()
    return render(request, 'myapp/huesped_list.html', {'huespedes': huespedes})

# Actualizar un huésped
def update_huesped(request, pk):
    huesped = get_object_or_404(Huespedes, pk=pk)
    form = HuespedesForm(request.POST or None, instance=huesped)
    if form.is_valid():
        form.save()
        return redirect('huesped_list')
    return render(request, 'myapp/huesped_form.html', {'form': form})

# Eliminar un huésped
def delete_huesped(request, pk):
    huesped = get_object_or_404(Huespedes, pk=pk)
    if request.method == 'POST':
        huesped.delete()
        return redirect('huesped_list')
    return render(request, 'myapp/huesped_confirm_delete.html', {'huesped': huesped})


#Crear reserva

from django.shortcuts import render, redirect
from .models import Reserva  # Importa tu modelo Reserva
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReservaForm
from django.contrib import messages

def hacer_reserva(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        print("Datos recibidos del formulario:", request.POST)  # Depuración

        if form.is_valid():
            form.save()  # Guarda la reserva en la base de datos
            messages.success(request, "¡Reserva guardada correctamente!")
            return redirect( 'home')
        else:
            # Imprime errores del formulario en la consola para depuración
            print("Errores en el formulario:", form.errors)

            # Renderiza nuevamente el formulario con errores
            return render(
                request,
                'reserva_form.html',
                {
                    'form': form,
                    'errors': form.errors,  # Muestra errores al usuario si es necesario
                }
            )
    else:
        form = ReservaForm()
        return render(request, 'reserva_form.html', {'form': form})
    


def validar_checkin(request):
    if request.method == "POST":
        # Obtén la cédula de la persona desde el formulario
        cedula = request.POST.get('id')

        try:
            # Busca la reserva en la base de datos por cédula
            reserva = Reserva.objects.get(identificacion=cedula)
            
            # Redirige a la tarjeta de registro con los datos de la reserva
            return redirect('tarjeta_registro', id=reserva.id)
        except Reserva.DoesNotExist:
            # Muestra un mensaje de error si no encuentra la reserva
            messages.error(request, "No se encontró una reserva con esa cédula.")
            return render(request, 'checkin.html')

    return render(request, 'checkin.html')  # Si no es


def tarjeta_registro(request, id):
    reserva = Reserva.objects.get(id=id)
    
    return render(request, 'tarjeta_registro.html', {
        'reserva': reserva,
        'total_huespedes': reserva.total_huespedes  # Usamos la propiedad
    })



def checkin(request):
    if request.method == "POST":
        # Obtener el valor del botón que se presionó
        action = request.POST.get('action')

        if action == 'validar_reserva':
            # Lógica para validar la reserva
            identificacion = request.POST.get('id')

            # Buscar todas las reservas que coincidan con la identificación
            reservas = Reserva.objects.filter(identificacion=identificacion)

            if reservas.exists():
                if reservas.count() == 1:
                    # Si solo hay una reserva, la seleccionamos
                    reserva = reservas.first()
                    # Pasar los datos de la reserva a la plantilla
                    return render(request, 'tarjeta_registro.html', {'reserva': reserva})
                else:
                    # Si hay múltiples reservas, mostramos un mensaje de error
                    messages.error(request, "Se encontraron múltiples reservas con la misma identificación. Por favor, verifica los datos.")
                    return redirect('checkin')
            else:
                messages.error(request, "No se encontró ninguna reserva con esa identificación.")
                return redirect('checkin')

        elif action == 'validar_ocr':
            # Lógica futura para validación con OCR (por ahora solo muestra un mensaje)
            messages.success(request, "Funcionalidad de OCR en proceso.")
            return redirect('checkin')

    return render(request, 'checkin.html')








import re
from django.http import JsonResponse
from PIL import Image
import pytesseract

def procesar_cedula(request):
    if request.method == 'POST' and 'documento_adjunto' in request.FILES:
        # Cargar el archivo de la cédula
        documento = request.FILES['documento_adjunto']
        img = Image.open(documento)

        # Extraer texto con OCR
        texto_ocr = pytesseract.image_to_string(img)

        # Limpiar el texto extraído
        texto_ocr = re.sub(r'[^A-Za-z0-9\s\.\-:]', ' ', texto_ocr)  # Quitar caracteres no alfanuméricos
        texto_ocr = re.sub(r'\s+', ' ', texto_ocr).strip()  # Reducir espacios múltiples a uno solo
        print("Texto OCR limpio:\n", texto_ocr)

        # Corregir posibles errores comunes del OCR en el texto
        texto_ocr = texto_ocr.replace("APeuigos", "APELLIDOS")  # Corregir "APeuigos"
        texto_ocr = texto_ocr.replace("wovero", "NUMERO")  # Corregir "wovero" a "NUMERO"
        texto_ocr = texto_ocr.replace("reibisam", "NOMBRES")  # Corregir "reibisam"
        print("Texto OCR corregido:\n", texto_ocr)

        # Dividir el texto en líneas para facilitar la búsqueda de datos clave
        lineas = texto_ocr.splitlines()

        # Inicializar los datos
        datos = {'id': None, 'nombre': None, 'apellido': None, 'fecha_nacimiento': None}

        # Buscar línea por línea los datos relevantes
        for i, linea in enumerate(lineas):
            # Buscar número de identificación (sin puntos)
            if not datos['id']:
                match = re.search(r'\b\d{1,3}(\.\d{3}){2,3}\b', linea)
                if match:
                    # Eliminar los puntos del número de identificación
                    datos['id'] = match.group().replace('.', '')

            # Buscar fecha de nacimiento (formato 28-SEP-2000)
            if not datos['fecha_nacimiento']:
                match = re.search(r'\d{2}-[A-Z]{3}-\d{4}', linea)
                if match:
                    # Reemplazar guiones por barras
                    datos['fecha_nacimiento'] = match.group().replace('-', '/')

            # Buscar apellido y nombre (después de la palabra "APELLIDOS")
            if 'APELLIDOS' in linea:
                partes = linea.split('APELLIDOS')
                if len(partes) > 1:
                    datos['apellido'] = partes[1].strip()  # Los apellidos
                    nombre_apellido = datos['apellido'].split()
                    if len(nombre_apellido) > 1:
                        datos['apellido'] = nombre_apellido[0]  # Primer apellido
                        datos['nombre'] = " ".join(nombre_apellido[1:])  # Nombre completo
                    else:
                        datos['nombre'] = datos['apellido']  # En caso que no haya nombre

        # Imprimir los resultados extraídos para depuración
        print("Datos extraídos:", datos)

        # Validar si se encontraron todos los datos
        if not all([datos['id'], datos['fecha_nacimiento'], datos['apellido']]):  # Validar que al menos ID, fecha y apellido estén presentes
            print("Error: No se encontraron todos los datos:", datos)  # Depuración
            return JsonResponse({'error': 'No se pudo extraer toda la información de la cédula.', 'datos': datos}, status=400)

        # Devolver los datos como respuesta JSON
        return JsonResponse(datos)

    # Manejar caso donde no se envía un archivo
    return JsonResponse({'error': 'No se subió ningún documento'}, status=400)
