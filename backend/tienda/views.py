import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *

stripe.api_key = settings.STRIPE_SECRET_KEY

# ==========================================
# VISTAS PÚBLICAS (Catálogo, Categorías, Tejidos)
# ==========================================
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

class TejidoViewSet(viewsets.ModelViewSet):
    queryset = Tejido.objects.all()
    serializer_class = TejidoSerializer
    permission_classes = [AllowAny]

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny] 

    # NUEVA ACCIÓN: Devuelve los datos del usuario logueado
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

# ==========================================
# VISTAS PROTEGIDAS (Requieren Login/Token JWT)
# ==========================================
class EncargoViewSet(viewsets.ModelViewSet):
    queryset = Encargo.objects.all() # <--- SOLUCIÓN AL ERROR AQUÍ
    serializer_class = EncargoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtro de seguridad: El usuario solo ve sus propios artículos en el carrito
        return Encargo.objects.filter(id_usuario=self.request.user)
    
    def perform_create(self, serializer):
        # Firma el encargo con el usuario que está haciendo la petición
        serializer.save(id_usuario=self.request.user)
        
    @action(detail=False, methods=['post'])
    def finalizar_pedido(self, request):
        user = request.user 
        items_cesta = Encargo.objects.filter(id_usuario=user, estado='CARRITO')

        if not items_cesta.exists():
            return Response({'error': 'Cesta vacía'}, status=400)

        total_pago = sum(i.precio * i.cantidad for i in items_cesta)
        nuevo_pedido = Pedido.objects.create(id_usuario=user, total=total_pago)

        line_items_stripe = []
        for item in items_cesta:
            DetallePedido.objects.create(
                id_pedido=nuevo_pedido,
                id_producto=item.id_producto,
                id_encargo=item if not item.id_producto else None,
                precio_unitario=item.precio,
                cantidad=item.cantidad
            )
            
            line_items_stripe.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': item.producto_type},
                    'unit_amount': int(item.precio * 100),
                },
                'quantity': item.cantidad,
            })
            
            item.estado = 'PROCESADO'
            item.save()

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items_stripe,
                mode='payment',
                success_url='http://localhost:5173/pago-exito',
                cancel_url='http://localhost:5173/carrito',
            )
            return Response({'url': session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all() # <--- SOLUCIÓN AL ERROR AQUÍ
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Si es admin ve todos los pedidos, si es cliente solo ve los suyos
        if self.request.user.is_staff:
            return Pedido.objects.all().order_by('-fecha_pedido')
        return Pedido.objects.filter(id_usuario=self.request.user).order_by('-fecha_pedido')