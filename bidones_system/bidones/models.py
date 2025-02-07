from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    dni = models.IntegerField(unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
