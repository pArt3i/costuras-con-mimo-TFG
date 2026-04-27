import { createRouter, createWebHistory } from 'vue-router'
import TiendaView from '../views/Tienda.vue' 


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'tienda',
      component: TiendaView,
    },
    {
      path: '/producto/:id',
      name: 'producto-detalle',
      component: () => import('../views/ProductoDetalle.vue'),
      props: true
    },
    {
      path: '/encargo-personalizado',
      name: 'encargo',
      component: () => import('../views/EncargoForm.vue')
    },
    {
      path: '/carrito',
      name: 'carrito',
      component: () => import('../views/Carrito.vue')
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('../views/PerfilView.vue'),
      meta: { requiereAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiereAuth: true, requiereAdmin: true } 
    },
    {
      path: '/pago-exito',
      name: 'PagoExito',
      component: () => import('../views/PagoExito.vue')
    },
  ],
})

router.beforeEach((to, from) => {
  const token = localStorage.getItem('token');
  const esAdmin = localStorage.getItem('isAdmin') === 'true'; 
  if (to.meta.requiereAuth && !token) {
    return '/'; 
  }

  if (to.meta.requiereAdmin && !esAdmin) {
    alert('⛔ Acceso denegado. Área reservada para administradores.');
    return '/';
  }

  return true;
});

export default router