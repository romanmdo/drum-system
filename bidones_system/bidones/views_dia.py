from django.shortcuts import render, redirect
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

        cliente = Cliente.objects.get(id=cliente_id)

        Dia.objects.create(
            cliente=cliente,
            bidones_20L=bidones_20L,
            bidones_15L=bidones_15L,
            precio_total=precio_total,
            paga=paga,
            debe=debe
        )

        return redirect("lista_dia")  # Ajusta el nombre según tu vista

    clientes = Cliente.objects.all()
    return render(request, "bidones/index.html", {"clientes": clientes})



def lista_dia(request):
    # Obtener solo los clientes que ya tienen registros en "Día a Día"
    clientes_con_registro = Dia.objects.values_list('cliente_id', flat=True)
    clientes_en_diario = Cliente.objects.filter(id__in=clientes_con_registro)
    
    # Obtener todos los clientes para seleccionarlos (pero sin mostrarlos en la tabla)
    clientes_disponibles = Cliente.objects.exclude(id__in=clientes_con_registro)

    context = {
        'clientes_en_diario': clientes_en_diario,  # Solo clientes con datos en "Día a Día"
        'clientes_disponibles': clientes_disponibles,  # Todos los clientes para seleccionar
    }
    
    return render(request, 'lista-dia.html', context)



def agregar_dia(request):
    clientes = Cliente.objects.all()  # Obtener todos los clientes para mostrar en el dropdown

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        bidones_20L = request.POST.get("bidones_20L")
        bidones_15L = request.POST.get("bidones_15L")
        precio_total = request.POST.get("precio_total")
        paga = request.POST.get("paga")
        debe = request.POST.get("debe")

        # Verificar que los datos sean válidos
        try:
            bidones_20L = int(bidones_20L)
            bidones_15L = int(bidones_15L)
            precio_total = float(precio_total)
            paga = float(paga)
            debe = float(debe)
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
                debe=debe
            )
            messages.success(request, 'Pedido registrado correctamente.')
        except Cliente.DoesNotExist:
            messages.error(request, 'El cliente no existe.')

        return redirect("lista_dia")

    return render(request, "bidones/lista_dia.html", {'clientes': clientes})
 