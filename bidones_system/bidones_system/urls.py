from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from bidones import views, views_clientes, views_dia

# Función para verificar si el usuario es superusuario
def superuser_required(user):
    return user.is_superuser

# Decorador para restringir vistas a superusuarios
superuser_only = login_required(user_passes_test(superuser_required))

urlpatterns = [
    # Autenticación y acceso general
    path('', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio, name='inicio'),

    # Registro de clientes y días
    path('registro-clientes/', views.registro_clientes, name='registro_clientes'),

    path('registro-dia/', views.registro_dia, name='registro_dia'),

    # Gestión de clientes
    path('clientes/', views_clientes.lista_clientes, name='lista_clientes'),
    path('clientes/new/', views_clientes.nuevo_cliente, name='nuevo_cliente'),
    path('clientes/edit/<int:cliente_id>/', views_clientes.editar_cliente, name='editar_cliente'),
    path('clientes/delete/<int:cliente_id>/', views_clientes.eliminar_cliente, name='eliminar_cliente'),

    # Gestión de días
    path('lista-dia/', views.lista_dia, name='lista_dia'),
    path('agregar-dia/', views_dia.agregar_dia, name='agregar_dia'),

    # ________ AJAX ________ #
    path('obtener_clientes/', views_dia.obtener_clientes, name='obtener_clientes'),
]
