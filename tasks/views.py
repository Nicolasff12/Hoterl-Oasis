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

def estandar(request):
    return render(request, 'estandar.html')

def deluxe(request):
    return render(request, 'deluxe.html')

def suite(request):
    return render(request, 'suite.html')


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
            return render(request, 'check_in.html')

    return render(request, 'check_in.html')  # Si no es una solicitud POST, se muestra la página

def tarjeta_registro(request, id):
    reserva = Reserva.objects.get(id=id)
    
    return render(request, 'tarjeta_registro.html', {
        'reserva': reserva,
        'total_huespedes': reserva.total_huespedes  # Usamos la propiedad
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reserva

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
                    return render(request, 'check_in.html', {'reserva': reserva})
                else:
                    # Si hay múltiples reservas, mostramos un mensaje de error
                    messages.error(request, "Se encontraron múltiples reservas con la misma identificación. Por favor, verifica los datos.")
                    return render(request, 'check_in.html')  # Mantener en la misma página
            else:
                messages.error(request, "No se encontró ninguna reserva con esa identificación.")
                return render(request, 'check_in.html')  # Mantener en la misma página

        elif action == 'validar_ocr':
            # Lógica futura para validación con OCR (por ahora solo muestra un mensaje)
            messages.success(request, "Funcionalidad de OCR en proceso.")
            return render(request, 'check_in.html')  # Mantener en la misma página

    return render(request, 'check_in.html')  # Mantener en la misma página








def procesar_cedulas(request):
    if request.method == 'POST' and 'documento_adjunto' in request.FILES:
        documento = request.FILES['documento_adjunto']
        
        try:
            # Abrir la imagen
            img = Image.open(documento)

            # Extraer el texto usando OCR
            texto_ocr = pytesseract.image_to_string(img)

            # Limpiar el texto extraído
            texto_ocr = re.sub(r'[^A-Za-z0-9\s\.\-:]', ' ', texto_ocr)  # Eliminar caracteres no alfanuméricos
            texto_ocr = re.sub(r'\s+', ' ', texto_ocr).strip()

            # Buscar el número de cédula (ID) usando una expresión regular más robusta
            match = re.search(r'\b\d{1,3}(\.\d{3}){2,3}\b', texto_ocr)
            if match:
                cedula = match.group().replace('.', '')  # Limpiar la cédula
            else:
                cedula = None

            # Buscar el nombre y apellido
            nombre_apellido_match = re.search(r'([A-Z]+(?: [A-Z]+)*) PELLUIDOS ([A-Z]+(?: [A-Z]+)*)', texto_ocr)
            if nombre_apellido_match:
                apellido = nombre_apellido_match.group(1)
                nombre = nombre_apellido_match.group(2)
            else:
                nombre = apellido = None

            # Si no se encuentra la cédula o los datos, retornar un error
            if not cedula or not nombre or not apellido:
                return JsonResponse({'error': 'Cédula no encontrada o datos incompletos'}, status=404)

            # Devolver los datos en formato JSON
            return JsonResponse({
                'id': cedula,
                'nombre': nombre,
                'apellido': apellido
            })

        except Exception as e:
            return JsonResponse({'error': f'Error al procesar la imagen: {str(e)}'}, status=400)
    
    return JsonResponse({'error': 'No se subieron documentos'}, status=400)
