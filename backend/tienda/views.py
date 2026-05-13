import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class EncargoViewSet(viewsets.ModelViewSet):
    queryset = Encargo.objects.all()
    serializer_class = EncargoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Encargo.objects.filter(id_usuario=self.request.user)
    
    def perform_create(self, serializer):
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
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Si es admin ve todos los pedidos, si es cliente solo ve los suyos
        if self.request.user.is_staff:
            return Pedido.objects.all().order_by('-fecha_pedido')
        return Pedido.objects.filter(id_usuario=self.request.user).order_by('-fecha_pedido')

    # ---> NUEVA LÓGICA DE CORREOS <---
    
    def perform_update(self, serializer):
        estado_anterior = serializer.instance.estado
        pedido = serializer.save()
        if estado_anterior != pedido.estado:
            self.enviar_correo_actualizacion(pedido)

    def enviar_correo_actualizacion(self, pedido):
        asuntos = {
            'PAGADO': 'Tu pedido ha sido confirmado 💸',
            'EN_PREPARACION': '¡Estamos preparando tu pedido! 🧵',
            'ENVIADO': '¡Tu pedido va en camino! 🚚',
            'ENTREGADO': 'Pedido entregado. ¡Disfrútalo! 🎁',
            'CANCELADO': 'Tu pedido ha sido cancelado ❌'
        }
        asunto = asuntos.get(pedido.estado, f"Actualización de tu pedido #{pedido.id}")

        mensaje = f"""
        ¡Hola {pedido.id_usuario.username}!
        
        Te escribimos desde Costuras con Mimo para avisarte de que tu pedido #{pedido.id} ha cambiado de estado.
        
        Nuevo estado: {pedido.estado.replace('_', ' ')}
        Total del pedido: {pedido.total}€
        
        Puedes revisar los detalles de tu compra en tu perfil en cualquier momento:
        http://localhost:5173/perfil
        
        ¡Muchas gracias por confiar en nuestro taller artesanal!
        """
        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email='hello@demomailtrap.co',
                recipient_list=[pedido.id_usuario.email], 
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error al enviar el correo: {e}")