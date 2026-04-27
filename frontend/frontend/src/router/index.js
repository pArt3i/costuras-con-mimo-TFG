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
    // 👇 NUEVA RUTA DE ADMIN 👇
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      // Le ponemos dos candados: tiene que estar logueado Y ser admin
      meta: { requiereAuth: true, requiereAdmin: true } 
    },
    {
      path: '/pago-exito',
      name: 'PagoExito',
      component: () => import('../views/PagoExito.vue')
    },
  ],
})

// 👇 EL GUARDIA DE SEGURIDAD ACTUALIZADO 👇
router.beforeEach((to, from) => {
  const token = localStorage.getItem('token');
  // Leemos si es admin (localStorage guarda texto, así que comprobamos si es la palabra 'true')
  const esAdmin = localStorage.getItem('isAdmin') === 'true'; 

  // Si requiere autenticación y no hay token, a la calle (al inicio)
  if (to.meta.requiereAuth && !token) {
    return '/'; 
  }

  // Si requiere ser Admin y no lo es, le avisamos y a la calle
  if (to.meta.requiereAdmin && !esAdmin) {
    alert('⛔ Acceso denegado. Área reservada para administradores.');
    return '/';
  }

  return true;
});

export default router