from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SetPasswordForm 
from django.contrib.auth import get_user_model
from .forms import UsuarioForm  
from django.http import HttpResponseForbidden
from .models import Usuario


def inicio(request):
    return render(request, 'usuarios/base.html')  # Plantilla de dashboard principal

#Funcion que valida el tipo de ingreso como credenciales dependiendo el acceso

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Autenticación del usuario
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin/')  # Redirigir al admin
                else:
                    return redirect('home')  # Redirigir a página principal de usuario normal
            else:
                messages.error(request, 'Datos incorrectos')
                return render(request, 'usuarios/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})

#Se verifica si el login cuenta con credenciales creadas mediante superUser, si es el caso, se valida y tiene acceso a los empleados 

def login_admin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  # Verificamos si es un administrador
                login(request, user)
                messages.success(request, "Bienvenido administrador.")
                return redirect('gestion_usuarios')  # Redirige al panel de administración
            else:
                messages.error(request, "No tienes permisos de administrador.")
                return redirect('login')  # Redirige a login si no es admin
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

#Vista que permite la gestion de usuarios via administrador

@login_required
def gestion_usuarios(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()  # Si no es admin, denegar acceso

    usuarios = Usuario.objects.all()  # Obtenemos todos los usuarios
    return render(request, 'usuarios/gestion_usuarios.html', {'usuarios': usuarios})


#Vista que permite agregar usuarios via administrador

@login_required
def agregar_usuario(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()  # Si no es admin, denegar acceso

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('gestion_usuarios')  # Redirigir al panel de administración
    else:
        form = RegistroForm()

    return render(request, 'usuarios/agregar_usuario.html', {'form': form})


#Vista que permite editar usuarios via administrador


@login_required
def editar_usuario(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()  # Si no es admin, denegar acceso

    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado exitosamente.")
            return redirect('gestion_usuarios')  # Redirigir al panel de administración
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


#Vista que permite eliminar usuarios via administrador


@login_required
def eliminar_usuario(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()  # Si no es admin, denegar acceso

    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado exitosamente.")
        return redirect('gestion_usuarios')  # Redirigir al panel de administración

    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})


#Vista que permite el registro para nuevos empleados u usuarios de la app

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, "Registro exitoso.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


#Funcion que permite la restauracion de contraseña generando un token y enviandolo via gmail, siempre y cuando el correo registrado este asociado a una cuenta
#de google, de lo contrario,este correo no llegara.

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            try:
                user = User.objects.get(email=email)
                
                # Generar un token de restablecimiento
                token = default_token_generator.make_token(user)
                
                # Codificar el ID de usuario
                uid = urlsafe_base64_encode(user.pk.encode())
                
                # Crear el enlace de restablecimiento
                reset_url = f'http://127.0.0.1:8000/reset_password/{uid}/{token}/'  # Enlace de restablecimiento
                
                # Configurar el mensaje del correo
                subject = 'Solicitud de restablecimiento de contraseña'
                message = f'Hola {user.username},\n\nHemos recibido una solicitud para restablecer tu contraseña. Si no fuiste tú, ignora este mensaje. Si deseas restablecerla, haz clic en el siguiente enlace:\n\n{reset_url}\n\nSaludos.'
                from_email = 'tu_correo@gmail.com'  # Cambia este correo por el que desees usar
                recipient_list = [email]

                # Enviar el correo
                send_mail(subject, message, from_email, recipient_list)

                messages.success(request, "Te hemos enviado un correo para restablecer tu contraseña.")
                return redirect('password_reset_done')
            except User.DoesNotExist:
                messages.error(request, "No encontramos ninguna cuenta con ese correo electrónico.")
                return redirect('password_reset')

    else:
        form = PasswordResetForm()

    return render(request, 'usuarios/password_reset.html', {'form': form})


#Redireccion a la pagina mediante enlace enviado via gmail, el cual permite realizar la actualizacion de contraseña y redireccion a login.

def reset_password(request, uidb64, token):
    try:
        # Decodificar el uid
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        
        # Verificar si el token es válido
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Tu contraseña ha sido restablecida correctamente.')
                    return redirect('login')  # Redirige a la página de inicio de sesión
            else:
                form = SetPasswordForm(user)
            
            return render(request, 'usuarios/reset_password.html', {'form': form})
        else:
            messages.error(request, 'El enlace de restablecimiento de contraseña no es válido o ha expirado.')
            return redirect('password_reset')
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido o ha expirado.')
        return redirect('password_reset')