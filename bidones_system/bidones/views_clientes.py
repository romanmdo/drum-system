from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.contrib import messages

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'bidones/lista_clientes.html', {'clientes': clientes})

def nuevo_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')

        if Cliente.objects.filter(dni=dni).exists():
            messages.error(request, "El cliente ya está registrado.")
        else:
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
            )
            messages.success(request, "Cliente añadido exitosamente.")
        return redirect('lista_clientes')
    return render(request, 'bidones/nuevo_cliente.html')


def editar_cliente(request, DNI):
    clientes = Cliente.objects.filter(dni_id = DNI)
    clientes_editar = Cliente.objects.get(dni=int(request.get['DNI']))
    return render(request, 'bidones/lista_clientes.html', {
        'mensaje': '',
        'clientes': clientes,
        'clientes_edit': clientes_editar,
    })

def guardar_editado(request):
    DNI = request.POST['DNI']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    telefono = request.POST['telefono']

    Cliente.objects.filter(dni=DNI).update(nombre=nombre, apellido=apellido, dni=DNI, telefono=telefono)
    clientes = Cliente.objects.filter(dni_id = DNI)

    return render(request, 'bidones/lista_clientes', {
        'mensaje': 'Se editó correctamente',
        'clientes': clientes,
    })