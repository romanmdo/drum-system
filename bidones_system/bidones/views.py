from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.contrib import messages

# Create your views here.

def inicio(request):
    return render(request, 'bidones/index.html')

def crud(request):
    return render(request, 'bidones/crud.html')

def lista_clientes(request):
    clientes = Cliente.objects.all()  # Obtener todos los clientes de la base de datos
    return render(request, 'bidones/lista_clientes.html', {'clientes': clientes})

def nuevo_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        dni = request.POST.get('dni')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')

        if Cliente.objects.filter(dni=dni).exists():
            messages.error(request, "El cliente ya está registrado.")
        else:
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                email=email,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
            )
            messages.success(request, "Cliente añadido exitosamente.")
        return redirect('lista_clientes')
    return render(request, 'bidones/nuevo_cliente.html')