import { createRouter, createWebHistory } from 'vue-router'
import TiendaView from '../views/Tienda.vue'
import Contacto from '../views/Contacto.vue' 


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
      meta: { requiereAuth: true, requiereAdmin: true, ocultarNav: true } 
    },
    {
      path: '/pago-exito',
      name: 'PagoExito',
      component: () => import('../views/PagoExito.vue')
    },
    {
      path: '/:pathMatch(.*)*', 
      name: 'NotFound',
      component: () => import('../views/Errors/NotFoundView.vue'),
      // Agregamos esto:
      meta: { ocultarNav: true }
    },
    {
      path: '/403',
      name: 'Forbidden',
      component: () => import('../views/Errors/ForbiddenView.vue'),
      meta: { ocultarNav: true }
    },
    {
      path: '/contacto',
      name: 'Contacto',
      component: Contacto
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
    return '/403';
  }

  return true;
});

export default router