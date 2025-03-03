from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.contrib import messages
from django.core.paginator import Paginator

def lista_clientes(request):
    clientes = Cliente.objects.all()
    paginator = Paginator(clientes, 5)  # 5 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtener grupo del primer cliente si no se pasa como parámetro
    grupo = request.GET.get('grupo')
    if not grupo:
        primer_cliente = Cliente.objects.first()
        grupo = primer_cliente.grupo if primer_cliente else 1  # Si no hay clientes, asigna grupo 1 por defecto

    return render(request, 'bidones/lista_clientes.html', {'page_obj': page_obj, 'grupo': grupo})


def nuevo_cliente(request, grupo):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        bidones_cantidad = request.POST.get('bidones_cantidad')
        observaciones = request.POST.get('observaciones')

        grupo_seleccionado = request.POST.get('grupo')  # ✅ Ahora tomamos el grupo del formulario

        if Cliente.objects.filter(direccion=direccion).exists():
            messages.error(request, "El cliente ya está registrado.")
        else:
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                telefono=telefono,
                direccion=direccion,
                grupo=grupo_seleccionado,  # ✅ Se asigna correctamente el grupo seleccionado
                bidones_cantidad=bidones_cantidad,
                observaciones=observaciones
            )
            messages.success(request, "Cliente añadido exitosamente.")
        return redirect("registro_clientes", grupo=grupo_seleccionado)  # ✅ Se redirige al grupo correcto
    
    return render(request, 'bidones/nuevo_cliente.html', {'grupo': grupo})

def editar_cliente(request, cliente_direccion):
    cliente = get_object_or_404(Cliente, id=cliente_direccion)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        grupo = request.POST.get('grupo')
        bidones_cantidad = request.POST.get('bidones_cantidad')
        observaciones = request.POST.get('observaciones')

        if Cliente.objects.filter(direccion=direccion).exclude(id=cliente_direccion).exists():
            messages.error(request, "La dirección ingresado ya pertenece a otro cliente.")
        else:
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.dni = dni
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.grupo = grupo
            cliente.bidones_cantidad = bidones_cantidad
            cliente.observaciones = observaciones
            cliente.save() 

            messages.success(request, "Cliente actualizado exitosamente.")
            return redirect('registro_clientes', grupo=cliente.grupo)

    return render(request, 'bidones/editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)  # Buscar el cliente o devolver 404
    cliente.delete()  # Eliminar cliente
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('lista_clientes')  # Cambia 'lista_clientes' por la URL correcta