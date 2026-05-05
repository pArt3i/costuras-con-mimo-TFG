<template>
  <div id="app">
    <nav v-if="!$route.meta.ocultarNav" class="navbar">
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
      v-if="!$route.meta.ocultarNav"
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