from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django import forms

#Registro de formulario donde incluyen los datos de validacion para un registro cono nombre, apellido, correo, contraseñas etc..

class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

#Registro de formulario donde incluyen los datos inicio de sesion


class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico')
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')

    
#Cambio de datos si se ingresa via administrador    

class UsuarioForm(UserChangeForm):
    # Definimos los campos que quieres que los administradores puedan modificar
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']

    # Añadimos un campo para confirmar la contraseña si es necesario
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=False)

    def clean_password(self):
        # Si el campo de la contraseña está vacío, no realizamos validaciones adicionales
        password = self.cleaned_data.get('password')
        if password:
            return password
        return None


