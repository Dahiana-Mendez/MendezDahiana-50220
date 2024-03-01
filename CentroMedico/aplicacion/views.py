from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms      import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins  import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, "aplicacion/home.html")

#LOGIN
def login_request(request):
    if request.method == "POST":
        usuario = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar
            

            return render(request, "aplicacion/home.html")
        else:
            return redirect(reverse_lazy('login'))
        
    miForm = AuthenticationForm()

    return render(request, "aplicacion/login.html", {"form": miForm })   

#LOGOUT
def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy ('home'))

#REGISTRACIÓN
def registro_usuario(request):
    if request.method == "POST":
        miForm = UserRegistroForm(request.POST)
        if miForm.is_valid():
            user = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('home'))

    else:    
        miForm = UserRegistroForm()

    return render(request, "aplicacion/registro_usuarios.html", {"form": miForm })  

#EDITAR PERFIL DE USUARIO
@login_required
def editar_perfil(request):
    usuario = request.user

    if request.method == "POST":
        miform = UsuarioEditForm(request.POST)
        if miform.is_valid():
            informacion = miform.cleaned_data
            user = User.objects.get(username=usuario)
            user.email = informacion['email']
            user.first_name = informacion['first_name']
            user.last_name = informacion['last_name']
            user.set_password(informacion['password1'])
            user.save()
            return render(request, "aplicacion/home.html")
    else:    
        miform = UsuarioEditForm(instance=usuario)

    return render(request, "aplicacion/editar_perfil.html", {"form": miform }) 

@login_required
def agregar_avatar(request):
    if request.method == "POST":
        miForm = Avatar_Formulario(request.POST, request.FILES)
        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)

           
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            
            avatar = Avatar(user=usuario, imagen=miForm.cleaned_data['imagen'])
            avatar.save()

           
            imagen = Avatar.objects.get(user=request.user.id).imagen.url
            request.session["avatar"] = imagen
            return render(request, "aplicacion/home.html")

    else:    
        miForm = Avatar_Formulario()

    return render(request, "aplicacion/agregar_Avatar.html", {"form": miForm })     


#PACIENTES
class PacienteList(LoginRequiredMixin, ListView):
    model = Paciente

class PacienteCreate(LoginRequiredMixin, CreateView):
    model = Paciente
    fields = ['nombre', 'apellido', 'fecha_nacimiento', 'edad', 'genero', 'telefono', 'correo_electronico']
    success_url = reverse_lazy('pacientes')

class PacienteUpdate(LoginRequiredMixin, UpdateView):
    model = Paciente
    fields = ['nombre', 'apellido', 'fecha_nacimiento', 'edad', 'genero', 'telefono', 'correo_electronico']
    success_url = reverse_lazy('pacientes')

class PacienteDelete(LoginRequiredMixin, DeleteView):
    model = Paciente
    success_url = reverse_lazy('pacientes')

#DOCTORES
class DoctorList(LoginRequiredMixin, ListView):
    model = Doctor

class DoctorCreate(LoginRequiredMixin, CreateView):
    model = Doctor
    fields = ['nombre', 'apellido', 'especialidad', 'telefono', 'correo_electronico']
    success_url = reverse_lazy('doctores')

class DoctorUpdate(LoginRequiredMixin, UpdateView):
    model = Doctor
    fields = ['nombre', 'apellido', 'especialidad', 'telefono', 'correo_electronico']
    success_url = reverse_lazy('doctores')

class DoctorDelete(LoginRequiredMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctores')

#CITAS
class CitaList(LoginRequiredMixin, ListView):
    model = Cita


def proximo_paciente(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    # Obtener la próxima cita para este doctor
    proxima_cita = Cita.objects.filter(doctor=doctor, fecha__gte=timezone.now()).order_by('fecha', 'hora').first()
    paciente = None
    if proxima_cita:
        paciente = proxima_cita.paciente
    return render(request, 'aplicacion/proximo_paciente.html', {'doctor': doctor, 'paciente': paciente})


class CitaCreate(LoginRequiredMixin, CreateView):
    model = Cita
    fields = ['paciente', 'doctor', 'fecha', 'hora']
    success_url = reverse_lazy('citas')

class CitaUpdate(LoginRequiredMixin, UpdateView):
    model = Cita
    fields = ['paciente', 'doctor', 'fecha', 'hora']
    success_url = reverse_lazy('citas')

class CitaDelete(LoginRequiredMixin, DeleteView):
    model = Cita
    success_url = reverse_lazy('citas')

#HISTORIAL MÉDICO   
class HistorialMedicoList(LoginRequiredMixin, ListView):
    model = HistorialMedico
    template_name = 'aplicacion/historialmedicolist.html'

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        queryset = HistorialMedico.objects.filter(paciente_id=paciente_id)
        return queryset 

class HistorialMedicoCreate(LoginRequiredMixin, CreateView):
    model = HistorialMedico
    fields = ['paciente', 'historial']
    success_url = reverse_lazy('pacientes')

class HistorialMedicoUpdate(LoginRequiredMixin, UpdateView):
    model = HistorialMedico
    fields = ['paciente', 'historial']
    success_url = reverse_lazy('pacientes')

class HistorialMedicoDelete(LoginRequiredMixin, DeleteView):
    model = HistorialMedico
    success_url = reverse_lazy('pacientes')


#BUSCAR
class PacienteBusquedaView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "aplicacion/paciente_list.html"

    def get_queryset(self):
        query = self.request.GET.get('buscar')
        paciente_list = Paciente.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query)
        ).distinct()

        return paciente_list


class DoctorBusquedaView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = "aplicacion/doctor_list.html"

    def get_queryset(self):
        query = self.request.GET.get('buscador')
        doctor_list = Doctor.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query)
        ).distinct()

        return doctor_list

#ACERCA DE MI  
def about(request):
    return render(request, 'aplicacion/acerca_de_mi.html', {})
       



 