from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.contrib import messages
from django.core.paginator import Paginator

def lista_clientes(request):
    clientes = Cliente.objects.all()
    paginator = Paginator(clientes, 5)  # 10 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bidones/lista_clientes.html', {'page_obj': page_obj})


def nuevo_cliente(request, grupo):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        if Cliente.objects.filter(dni=dni).exists():
            messages.error(request, "El cliente ya está registrado.")
        else:
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                direccion=direccion,
                grupo=grupo  # Usamos el 'grupo' de la URL
            )
            messages.success(request, "Cliente añadido exitosamente.")
        return redirect("registro_clientes", grupo=grupo)  # Redirigimos con el 'grupo'
    
    return render(request, 'bidones/nuevo_cliente.html', {'grupo': grupo})  # Pasamos el grupo a la plantilla


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        grupo = request.POST.get('grupo')

        if Cliente.objects.filter(dni=dni).exclude(id=cliente_id).exists():
            messages.error(request, "El DNI ingresado ya pertenece a otro cliente.")
        else:
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.dni = dni
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.grupo = grupo
            cliente.save() 

            messages.success(request, "Cliente actualizado exitosamente.")
            return redirect('lista_clientes')

    return render(request, 'bidones/editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)  # Buscar el cliente o devolver 404
    cliente.delete()  # Eliminar cliente
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('lista_clientes')  # Cambia 'lista_clientes' por la URL correcta