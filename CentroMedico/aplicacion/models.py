from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    
class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, null=True)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()

    def __str__(self):
        return f"{self.apellido}, {self.nombre}, {self.especialidad}"
    
class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"Cita con {self.doctor.nombre} el {self.fecha} a las {self.hora}"
    

class HistorialMedico(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    historial = models.TextField()
    
    def __str__(self):
        return f"Historial médico de {self.paciente.nombre}"

class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"   