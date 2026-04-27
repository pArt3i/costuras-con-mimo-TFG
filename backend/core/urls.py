from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tienda.views import ProductoViewSet, EncargoViewSet, CategoriaViewSet, TejidoViewSet, UsuarioViewSet, PedidoViewSet
from django.conf import settings             
from django.conf.urls.static import static   

# 👇 1. IMPORTA LAS VISTAS DE LOS TOKENS
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'encargos', EncargoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'tejidos', TejidoViewSet)
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'pedidos', PedidoViewSet),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)