from django.db import models

class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Dia(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    bidon_15l = models.IntegerField(unique=True)
    bidon_20l = models.IntegerField(unique=True)
    precio = models.IntegerField(unique=True)
    paga = models.IntegerField(unique=True)
    debe = models.IntegerField(unique=True)
    fecha = models.DateField(verbose_name='Fecha')
