from django.urls import path
from .views import *
from aplicacion import views


urlpatterns = [
    
    path('', home, name= "home" ),

    path('login/',login_request,name="login"),
    path('registro/',registro_usuario,name="registro"),
    path('logout/',custom_logout,name="logout"),
    path('editar_perfil/',editar_perfil,name="editar_perfil"),
    path('agregar_avatar/',agregar_avatar,name="agregar_avatar"),
    

    #PACIENTES
    path('Pacientes/', PacienteList.as_view(), name= "pacientes" ),
    path('Paciente_create/', PacienteCreate.as_view(), name= "Paciente_create" ),
    path('paciente_update/<int:pk>/', PacienteUpdate.as_view(), name="paciente_update"),
    path('Paciente_delete/<int:pk>/', PacienteDelete.as_view(), name= 'Paciente_delete' ),

    #DOCTORES
    path('Doctores/', DoctorList.as_view(), name= "doctores" ),
    path('doctor_create/', DoctorCreate.as_view(), name= "doctor_create" ),
    path('doctor_update/<int:pk>/', DoctorUpdate.as_view(), name="doctor_update"),
    path('doctor_delete/<int:pk>/', DoctorDelete.as_view(), name= 'doctor_delete' ),
    path('doctor/<int:doctor_id>/proximo_paciente/', views.proximo_paciente, name='proximo_paciente'),


    #CITA
    path('citas/', CitaList.as_view(), name= "citas" ),
    path('cita_create/', CitaCreate.as_view(), name= "cita_create" ),
    path('cita_update/<int:pk>/', CitaUpdate.as_view(), name="cita_update"),
    path('cita_delete/<int:pk>/', CitaDelete.as_view(), name= "cita_delete" ),

    #HISTORIAL MÉDICO
    path('historial_medico/<int:paciente_id>/', HistorialMedicoList.as_view(), name= "historial_medico" ),
    path('historialMedico_create/', HistorialMedicoCreate.as_view(), name= "historialMedico_create" ),
    path('historialMedico_update/<int:pk>/', HistorialMedicoUpdate.as_view(), name="historialMedico_update"),
    path('historialMedico_delete/<int:pk>/', HistorialMedicoDelete.as_view(), name="historialMedico_delete"),

    #BUSCAR
    path('buscar/', views.PacienteBusquedaView.as_view(), name='buscar'),
    path('buscador/', views.DoctorBusquedaView.as_view(), name='buscarDoctor'),
   


   path('acerca_de_mi/', views.about, name='acerca_de_mi'),

]