from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Cliente, Dia

def clientes_list(request):
    # Obtener todos los clientes desde la base de datos
    clientes = Cliente.objects.all()
    return render(request, 'bidones/clientes_list.html', {'clientes': clientes})


def agregar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')

        # Crear un nuevo cliente en la base de datos
        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            telefono=telefono
        )

        return redirect('clientes_list')  # Redirigir a la lista de clientes

    return HttpResponse("Método no permitido", status=405)


def eliminar_cliente(request, dni):
    # Obtener el cliente por su DNI
    cliente = get_object_or_404(Cliente, dni=dni)
    cliente.delete()

    return redirect('clientes_list')


def editar_cliente(request, dni):
    cliente = get_object_or_404(Cliente, dni=dni)

    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')
        cliente.save()

        return redirect('clientes_list')

    return render(request, 'bidones/editar_cliente.html', {'cliente': cliente})
