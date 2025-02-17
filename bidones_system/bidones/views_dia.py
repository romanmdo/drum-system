from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib import messages
from django.http import JsonResponse
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

        return redirect("lista_dia") # PRESTAR ATENCION, CAMBIAR ESA VISTA

    clientes = Cliente.objects.all()
    return render(request, "bidones/index.html", {"clientes": clientes})



def lista_dia(request):
    clientes = Cliente.objects.all()  # Obtiene todos los clientes
    
    paginator = Paginator(clientes, 10)  # Paginamos a 10 clientes por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual

    return render(request, 'bidones/lista_dia.html', {
        'clientes' : clientes,
        'page_obj' : page_obj,
        })




def agregar_dia(request):
    clientes = Cliente.objects.all()  # Obtener todos los clientes para mostrar en el dropdown

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
            print("BIDONES DE 12 LITROS recibido:", request.POST.get("bidones_15L"))
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

        return redirect("lista_dia")

    return render(request, "bidones/lista_dia.html", {'clientes': clientes})

# __________ PRUEBAS DE AJAX __________ #

def obtener_clientes(request):
    clientes = Cliente.objects.all().values('id', 'nombre')  # Devuelve solo los datos necesarios
    return JsonResponse(list(clientes), safe=False)  # Convierte QuerySet en lista JSON