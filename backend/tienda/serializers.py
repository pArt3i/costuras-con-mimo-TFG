from rest_framework import serializers
from .models import (
    Usuario, Categoria, Producto, 
    Tejido, Encargo, Pedido, DetallePedido
)

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TejidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tejido
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'is_superuser','password','direccion']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='id_categoria.nombre_cat')
    
    class Meta:
        model = Producto
        fields = ['id', 'id_categoria', 'categoria_nombre', 'nombre', 'precio', 'stock', 'img']

class EncargoSerializer(serializers.ModelSerializer):
    producto_img = serializers.ReadOnlyField(source='id_producto.img')
    tejido_nombre = serializers.ReadOnlyField(source='id_tejido.nombre_tej')
    
    class Meta:
        model = Encargo
        fields = '__all__'
        read_only_fields = ['id_usuario']

class DetallePedidoSerializer(serializers.ModelSerializer):
    nombre_item = serializers.SerializerMethodField()
    imagen_item = serializers.SerializerMethodField()
    
    class Meta:
        model = DetallePedido
        fields = '__all__'
        
    def get_nombre_item(self, obj):
        if obj.id_producto: 
            return obj.id_producto.nombre
        if obj.id_encargo: 
            return f"Personalizado: {obj.id_encargo.producto_type}"
        return "Artículo"

    def get_imagen_item(self, obj):
        if obj.id_producto: 
            return obj.id_producto.img
        if obj.id_encargo and obj.id_encargo.id_tejido: 
            return obj.id_encargo.id_tejido.img
        return None

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    usuario_nombre = serializers.ReadOnlyField(source='id_usuario.username')
    
    class Meta:
        model = Pedido
        fields = '__all__'