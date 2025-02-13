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


def editar_cliente(request, cliente_id):
    # Obtener el cliente o devolver un 404 si no existe
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')

        # Validar si el DNI ya pertenece a otro cliente
        if Cliente.objects.filter(dni=dni).exclude(id=cliente_id).exists():
            messages.error(request, "El DNI ingresado ya pertenece a otro cliente.")
        else:
            # Actualizar los datos del cliente
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.dni = dni
            cliente.telefono = telefono
            cliente.save()  # Guardar los cambios en la base de datos

            messages.success(request, "Cliente actualizado exitosamente.")
            return redirect('lista_clientes')

    # Renderizar el formulario con los datos del cliente existente
    return render(request, 'bidones/editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)  # Buscar el cliente o devolver 404
    cliente.delete()  # Eliminar cliente
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('lista_clientes')  # Cambia 'lista_clientes' por la URL correcta