"""
URL configuration for sistema_usuarios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from usuarios import views as usuarios_views
from django.contrib.auth import views as auth_views #Ruta de recuperacion de contraseña
from usuarios import views

urlpatterns = [
    
    #Ruta de panel de administracion
    path('admin/', admin.site.urls),
    
    #Rutas de inicio de sesion y registro como de dashboard de la pagina(inicio)
    path('registro/', usuarios_views.registro, name='registro'),
    path('login/', usuarios_views.iniciar_sesion, name='login'),
    path('inicio/', usuarios_views.inicio, name='inicio'),  # NUEVA RUTA

    
    #Gestión de usuarios (solo para administradores)
    path('gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('editar-usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    #Recuperación de contraseña : 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'),
]
