from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    direccion = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField('auth.Group', related_name='usuario_tienda_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuario_tienda_permissions', blank=True)

class Categoria(models.Model):
    nombre_cat = models.CharField(max_length=100)
    def __str__(self): return self.nombre_cat

class Producto(models.Model):
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    stock = models.IntegerField()
    img = models.CharField(max_length=500)
    def __str__(self): return self.nombre

class ProductoImagen(models.Model):
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes_extra')
    img_url = models.CharField(max_length=500)
    orden = models.IntegerField(default=0)

class Tejido(models.Model):
    nombre_tej = models.CharField(max_length=100)
    img = models.CharField(max_length=500)
    def __str__(self): return self.nombre_tej

class Encargo(models.Model):
    ESTADOS = [('CARRITO', 'Carrito'), ('PROCESADO', 'Procesado')]
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    id_tejido = models.ForeignKey(Tejido, on_delete=models.SET_NULL, null=True, blank=True)
    producto_type = models.CharField(max_length=100)
    bordado = models.CharField(max_length=100, blank=True)
    precio = models.FloatField(default=0.0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='CARRITO')
    cantidad = models.IntegerField(default=1)
    fecha_enc = models.DateTimeField(auto_now_add=True)

# --- LA TABLA DE PEDIDOS (CABECERA) ---
class Pedido(models.Model):
    ESTADOS_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('EN_PREPARACION', 'En Preparación'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0.0)
    direccion = models.CharField(max_length=255, blank=True, null=True) # Añadido por tu diagrama
    estado = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='PENDIENTE')

    def __str__(self): return f"Pedido {self.id} - {self.id_usuario.username}"

# --- LA TABLA DETALLE_PEDIDO (LÍNEAS) ---
class DetallePedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    
    # Puede ser un producto estándar de la tienda...
    id_producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    
    # ... O puede ser un encargo personalizado
    id_encargo = models.ForeignKey(Encargo, on_delete=models.SET_NULL, null=True, blank=True)
    
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.FloatField()