from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib import messages
from .models import Cliente, Dia

def registrar_dia(request):
    if request.method == "POST":
        cliente_id = request.POST["cliente"]
        bidones_20L = int(request.POST["bidones_20L"])
        bidones_15L = int(request.POST["bidones_15L"])
        precio_total = float(request.POST["precio_total"])
        paga = float(request.POST["paga"])
        debe = float(request.POST["debe"])
        alquila = int(request.POST["alquila"])

        cliente = Cliente.objects.get(id=cliente_id)

        Dia.objects.create(
            cliente=cliente,
            bidones_20L=bidones_20L,
            bidones_15L=bidones_15L,
            precio_total=precio_total,
            paga=paga,
            debe=debe,
            alquila=alquila
        )

        return redirect("lista_dia", grupo=cliente.grupo) # PRESTAR ATENCION, CAMBIAR ESA VISTA

    clientes = Cliente.objects.all().order_by('id')  # O cualquier campo por el que quieras ordenar
    return render(request, "bidones/index.html", {"clientes": clientes})


def agregar_dia(request):
    clientes = Cliente.objects.all().order_by('id')

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        bidones_20L = request.POST.get("bidones_20L")
        bidones_15L = request.POST.get("bidones_15L")
        precio_total = request.POST.get("precio_total")
        paga = request.POST.get("paga")
        debe = request.POST.get("debe")
        alquila = request.POST.get('alquila')

        # Verificar que los datos sean válidos
        try:
            bidones_20L = int(bidones_20L)
            bidones_15L = int(bidones_15L)
            precio_total = float(precio_total)
            paga = float(paga)
            debe = float(debe)
            alquila = int(alquila)
        except ValueError:
            messages.error(request, "Por favor ingrese valores válidos en los campos numéricos.")
            return render(request, "bidones/lista_dia.html", {'clientes': clientes})

        # Verificar si el cliente existe
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            # Crear el nuevo registro de "Día"
            nuevo_dia = Dia.objects.create(
                cliente=cliente,
                bidones_20L=bidones_20L,
                bidones_15L=bidones_15L,
                precio_total=precio_total,
                paga=paga,
                debe=debe,
                alquila=alquila
            )
            messages.success(request, 'Pedido registrado correctamente.')
        except Cliente.DoesNotExist:
            messages.error(request, 'El cliente no existe.')
            return render(request, "bidones/lista_dia.html", {'clientes': clientes})

        # Imprimir el grupo antes de la redirección
        print(f"Redirigiendo a grupo: {cliente.grupo}")
        return redirect("lista_dia", grupo=cliente.grupo)

    return render(request, "bidones/lista_dia.html", {'clientes': clientes})

def editar_dia(request, dia_id):
    # Obtener el registro de Día o devolver error 404 si no existe
    dia = get_object_or_404(Dia, id=dia_id)
    clientes = Cliente.objects.all().order_by('id')  # Para mostrar en el formulario

    if request.method == "POST":
        # Obtener datos del formulario
        cliente_id = request.POST.get("cliente")
        bidones_20L = request.POST.get("bidones_20L")
        bidones_15L = request.POST.get("bidones_15L")
        precio_total = request.POST.get("precio_total")
        paga = request.POST.get("paga")
        debe = request.POST.get("debe")
        alquila = request.POST.get("alquila")

        # Validar datos
        try:
            bidones_20L = int(bidones_20L)
            bidones_15L = int(bidones_15L)
            precio_total = float(precio_total)
            paga = float(paga)
            debe = float(debe)
            alquila = int(alquila)
        except ValueError:
            messages.error(request, "Por favor ingrese valores válidos en los campos numéricos.")
            return render(request, "bidones/editar_dias.html", {'dia': dia, 'clientes': clientes})

        # Verificar si el cliente existe
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, "El cliente seleccionado no existe.")
            return render(request, "bidones/editar_dias.html", {'dia': dia, 'clientes': clientes})

        # Actualizar los datos del registro
        dia.cliente = cliente
        dia.bidones_20L = bidones_20L
        dia.bidones_15L = bidones_15L
        dia.precio_total = precio_total
        dia.paga = paga
        dia.debe = debe
        dia.alquila = alquila
        dia.save()  # Guardar cambios

        messages.success(request, "Registro actualizado correctamente.")
        return redirect("lista_dia", grupo=cliente.grupo)  # Redirigir a la lista de días

    return render(request, "bidones/editar_dias.html", {"dia": dia, "clientes": clientes})

def lista_dia(request, grupo):
    # Filtrar los clientes por grupo
    clientes = Cliente.objects.filter(grupo=grupo)
    
    # Filtrar los registros de días por grupo
    dias = Dia.objects.filter(cliente__grupo=grupo).order_by('id')
    
    # Paginación de los registros de días
    paginator = Paginator(dias, 10)  # Paginamos a 10 registros de "Día" por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual
    
    return render(request, 'bidones/lista_dia.html', {
        'clientes': clientes,
        'dias': page_obj,  # Paginamos los días
        'grupo': grupo,
    })

def eliminar_dia(request, dia_id):
    dia = get_object_or_404(Dia, id=dia_id)  # Buscar el registro o devolver 404
    grupo = dia.cliente.grupo  # Obtener el grupo antes de eliminar
    dia.delete()  # Eliminar registro
    messages.success(request, "Registro eliminado correctamente.")
    return redirect("lista_dia", grupo=grupo)  # Redirigir a la lista de días

#def buscar_cliente(request):
#    query = request.GET.get("query", "").strip()  # Obtener la búsqueda y eliminar espacios extra
#    clientes = Cliente.objects.all()  # Obtener todos los clientes por defecto

#    if query:  # Si hay una búsqueda, filtramos los clientes
#        clientes = clientes.filter(nombre__icontains=query)  # Busca coincidencias en el nombre

#    return render(request, "bidones/lista_clientes.html", {"clientes": clientes, "query": query})