"""
URL configuration for bidones_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bidones import views
from bidones import views_clientes
from bidones import views_dia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio, name='inicio'),

    path('registro-clientes/', views.lista_clientes, name='lista_clientes'),
    path('registro-dia/', views.lista_dia, name='lista_dia'),
    
    path('clientes/new/', views_clientes.nuevo_cliente, name='nuevo_cliente'),
    path('clientes/edit/<int:cliente_id>/', views_clientes.editar_cliente, name='editar_cliente'),
    path('clientes/delete/<int:cliente_id>/', views_clientes.eliminar_cliente, name='eliminar_cliente'),

    path('dia/', views_dia.registrar_dia, name='registrar_dia'),
    path("registrar-dia/", views_dia.registrar_dia, name="registrar_dia"),
    path('agregar-dia/', views_dia.agregar_dia, name='agregar_dia'),

]
