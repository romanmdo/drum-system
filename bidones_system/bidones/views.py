from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Cliente, Dia 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/inicio/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'bidones/login.html')

def inicio(request):
    return render(request, 'bidones/index.html')

#def lista_clientes(request):
#    clientes = Cliente.objects.all()
#    paginator = Paginator(clientes, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'bidones/lista_clientes.html', {'page_obj': page_obj})

def ruta(request):
    return render(request, 'bidones/lista_ruta.html')

def superuser_required(user):
    """Verifica si el usuario es superusuario."""
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(superuser_required, login_url='/')
def lista_dia(request, grupo):
    # Obtener el valor de búsqueda desde el formulario
    search = request.GET.get('search', '').strip()
    
    # Filtrar los clientes por grupo
    clientes = Cliente.objects.filter(grupo=grupo)
    
    # Filtrar los registros de días por grupo y por búsqueda (apellido o fecha)
    dias = Dia.objects.filter(cliente__grupo=grupo)
    if search:
        dias = dias.filter(cliente__apellido__icontains=search) | dias.filter(fecha__icontains=search)

    # Paginación de los registros de días
    paginator = Paginator(dias.order_by('id'), 10)  # Paginamos a 10 registros de "Día" por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual
    
    return render(request, 'bidones/lista_dia.html', {
        'clientes': clientes,
        'dias': page_obj,  # Paginamos los días
        'grupo': grupo,
        'search': search,  # Mantener el término de búsqueda
    })

@login_required(login_url='/login/')
@user_passes_test(superuser_required, login_url='/')
@login_required(login_url='/login/')
@user_passes_test(superuser_required, login_url='/')
def registro_clientes(request, grupo):
    # Obtener el término de búsqueda desde el formulario
    search = request.GET.get('search', '').strip()
    
    # Filtrar los clientes por grupo
    clientes = Cliente.objects.filter(grupo=grupo)

    # Aplicar la búsqueda por apellido o nombre
    if search:
        clientes = clientes.filter(apellido__icontains=search) | clientes.filter(nombre__icontains=search)

    # Paginación
    paginator = Paginator(clientes.order_by('nombre'), 5)  # 5 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bidones/lista_clientes.html', {
        'page_obj': page_obj,
        'grupo': grupo,
        'search': search  # Mantener el término de búsqueda
    })


@login_required(login_url='/login/')
@user_passes_test(superuser_required, login_url='/')
def registro_dia(request):
    return render(request, 'bidones/lista_dia.html')
