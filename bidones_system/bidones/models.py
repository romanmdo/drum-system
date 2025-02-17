from django.db import models

class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=100)

    class Meta:
        db_table = "bidones_cliente"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Dia(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    bidones_20L = models.IntegerField(default=0)
    bidones_15L = models.IntegerField(default=0)
    alquila = models.IntegerField(default=0)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    paga = models.DecimalField(max_digits=10, decimal_places=2)
    debe = models.DecimalField(max_digits=10, decimal_places=2) 
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Registro de {self.cliente.nombre} {self.cliente.apellido} - {self.fecha}"
