<template>
  <div id="app">
    <nav v-if="$route.path !== '/admin'" class="navbar">
      <div class="nav-links">
        <router-link to="/" class="nav-link">Tienda</router-link>
        <router-link to="/encargo-personalizado" class="nav-link">Encargos</router-link>
        
        <router-link v-if="isAdmin" to="/admin" class="nav-link" style="color: #bc6c25;">
          ⚙️ Panel Admin
        </router-link>
      </div>

      <div class="nav-auth">
        <router-link to="/carrito" class="cart-icon">
          🛒 <span v-if="cartCount > 0" class="badge">{{ cartCount }}</span>
        </router-link>
        
        <button v-if="!token" @click="mostrarModal = true" class="btn-login">Acceder</button>
        
        <div v-else style="display: flex; gap: 10px; align-items: center;">
          <button @click="irAlPerfil" class="btn-perfil">👤 {{ nombreUsuario }}</button>
          <button @click="cerrarSesion" class="btn-logout">Salir</button>
        </div>
      </div>
    </nav>

    <router-view />

    <LoginModal 
      v-if="$route.path !== '/admin'"
      :mostrar="mostrarModal" 
      @cerrar="mostrarModal = false" 
      @loginExitoso="actualizarEstado" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import LoginModal from './components/LoginModal.vue'

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

// Cuenta los productos en estado CARRITO
const actualizarContadorCarrito = async () => {
  if (!token.value) return; // Si no hay usuario, no hay carrito que contar
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

<style>
/* Estilos globales y de la Navbar */
body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fdfaf0; }
.navbar { background: #ccd5ae; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.nav-links { display: flex; gap: 20px; }
.nav-link { text-decoration: none; color: #333; font-weight: bold; transition: color 0.3s; font-size: 1.1rem; }
.nav-link:hover { color: #606c38; }
.nav-auth { display: flex; gap: 20px; align-items: center; }
.cart-icon { text-decoration: none; font-size: 1.5rem; position: relative; }
.badge { background: #d9534f; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.75rem; position: absolute; top: -5px; right: -10px; font-weight: bold; }
.btn-login { background: #606c38; color: white; border: none; padding: 8px 20px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: background 0.2s; }
.btn-login:hover { background: #4a532a; }
.btn-perfil { background: #bc6c25; color: white; border: none; padding: 8px 20px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: background 0.2s; }
.btn-perfil:hover { background: #96561d; }
.btn-logout { background: transparent; color: #d9534f; border: 1px solid #d9534f; padding: 6px 15px; border-radius: 20px; cursor: pointer; font-weight: bold; transition: 0.2s; }
.btn-logout:hover { background: #d9534f; color: white; }
</style>