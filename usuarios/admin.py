from django.contrib import admin
from .models import Usuario

#Aqui en admin se se filtran los campos del usuario admin ( otorga los accesos especiales )

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

admin.site.register(Usuario, UsuarioAdmin)  
