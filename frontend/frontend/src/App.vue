<template>
  <div id="app">
    
    <!-- NUEVO HEADER DE DOS FRANJAS -->
    <header v-if="!$route.meta.ocultarNav" class="header-principal">
      
      <!-- Franja Superior (Logo, Admin, Usuario y Carrito) -->
      <div class="header-top">
        
        <!-- Izquierda: Link del Admin (para equilibrar visualmente) -->
        <div class="header-izq">
          <router-link v-if="isAdmin" to="/admin" class="enlace-admin">
            ⚙️ Panel Admin
          </router-link>
        </div>

        <!-- Centro: Logo y Título -->
        <div class="header-centro">
          <router-link to="/" class="logo-wrapper">
            <!-- Icono de aguja e hilo dibujado con SVG -->
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#606c38" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4.5 19.5l15-15M13.5 4.5l6 6M4 20c-2 0-3-1-3-3 0-2 2-3 4-2 2 1 3 3 2 4s-3 1-3 1z" />
            </svg>
            <span class="logo-texto">Costuras con Mimo</span>
          </router-link>
        </div>

        <!-- Derecha: Login y Carrito -->
        <div class="header-der">
          <div v-if="!token" class="auth-box">
            <button @click="mostrarModal = true" class="btn-login-header">👤 Iniciar sesión</button>
          </div>
          <div v-else class="auth-box">
            <span class="user-greeting" @click="irAlPerfil" title="Ir a mi perfil">
              👤 Hola, {{ nombreUsuario }}
            </span>
            <button @click="cerrarSesion" class="btn-logout-mini">Salir</button>
          </div>

          <router-link to="/carrito" class="btn-carrito-header">
            🛒 <span class="cart-count">{{ cartCount }} {{ cartCount === 1 ? 'item' : 'items' }}</span>
          </router-link>
        </div>
      </div>

      <!-- Franja Inferior (Menú de Navegación Verde) -->
      <nav class="header-bottom">
        <router-link to="/" class="nav-bottom-link" exact-active-class="activo">INICIO</router-link>
        <router-link to="/encargo-personalizado" class="nav-bottom-link" exact-active-class="activo">PIDE TU ENCARGO</router-link>
        <router-link to="/contacto" class="nav-bottom-link" exact-active-class="activo">CONTACTO</router-link>
      </nav>
      
    </header>

    <!-- Contenido de la página -->
    <router-view class="contenido-principal" />

    <!-- Modales y Footer -->
    <LoginModal 
      v-if="!$route.meta.ocultarNav"
      :mostrar="mostrarModal" 
      @cerrar="mostrarModal = false" 
      @loginExitoso="actualizarEstado" 
    />

    <FooterTienda v-if="!$route.meta.ocultarNav" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import LoginModal from './components/LoginModal.vue'
import FooterTienda from './components/FooterTienda.vue'

const router = useRouter()
const token = ref(localStorage.getItem('token'))
const nombreUsuario = ref(localStorage.getItem('username'))
const isAdmin = ref(localStorage.getItem('isAdmin') === 'true')
const mostrarModal = ref(false)
const cartCount = ref(0) 

const actualizarEstado = () => {
  token.value = localStorage.getItem('token')
  nombreUsuario.value = localStorage.getItem('username')
  isAdmin.value = localStorage.getItem('isAdmin') === 'true' 
  mostrarModal.value = false
  actualizarContadorCarrito()
}

const cerrarSesion = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('isAdmin')
  token.value = null
  nombreUsuario.value = ''
  isAdmin.value = false
  cartCount.value = 0
  router.push('/')
}

const irAlPerfil = () => {
  router.push('/perfil')
}

const actualizarContadorCarrito = async () => {
  if (!localStorage.getItem('token')) return;
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/encargos/')
    const itemsEnCarrito = response.data.filter(encargo => encargo.estado === 'CARRITO')
    cartCount.value = itemsEnCarrito.length
  } catch (error) {
    console.error("Error al contar los items del carrito:", error)
  }
}

onMounted(() => {
  actualizarContadorCarrito()
  window.addEventListener('carrito-actualizado', actualizarContadorCarrito)
})

onUnmounted(() => {
  window.removeEventListener('carrito-actualizado', actualizarContadorCarrito)
})
</script>