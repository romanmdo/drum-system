from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

def inicio(request):
    return render(request, 'bidones/index.html')

def lista_clientes(request):
    clientes = Cliente.objects.all()
    paginator = Paginator(clientes, 10)  # 10 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bidones/lista_clientes.html', {'page_obj': page_obj})

def lista_dia(request):
    clientes = Cliente.objects.all()  # Obtener todos los clientes de la base de datos
    return render(request, 'bidones/lista_dia.html', {'clientes': clientes})