from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Logística', {'fields': ('direccion',)}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Categoria)
admin.site.register(Tejido)
admin.site.register(ProductoImagen)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')

@admin.register(Encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_usuario', 'producto_type', 'estado', 'precio')
    list_filter = ('estado',)