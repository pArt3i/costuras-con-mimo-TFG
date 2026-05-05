<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// --- ESTADO DEL PERFIL ---
const usuario = ref({
  username: 'Cargando...',
  email: '',
  direccion: ''
})

const pedidos = ref([])
const cargando = ref(true)

// --- ESTADO DEL MODAL DE PEDIDOS ---
const modalAbierto = ref(false)
const pedidoSeleccionado = ref(null)

const cargarDatos = async () => {
  try {
    const nombreGuardado = localStorage.getItem('username')
    const token = localStorage.getItem('token')

    // 1. OBTENER LOS DATOS REALES DEL USUARIO DESDE EL BACKEND
    if (nombreGuardado && token) {
      const userRes = await axios.get('http://127.0.0.1:8000/api/usuarios/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      // Buscamos al usuario conectado en la lista
      const miUsuario = userRes.data.find(u => u.username === nombreGuardado)
      
      if (miUsuario) {
        usuario.value = {
          username: miUsuario.username,
          email: miUsuario.email || 'No especificado',
          direccion: miUsuario.direccion || 'No especificada' // Carga la de la base de datos
        }
      }
    }

    // 2. OBTENER LOS PEDIDOS
    const response = await axios.get('http://127.0.0.1:8000/api/pedidos/')
    
    if (nombreGuardado) {
      pedidos.value = response.data.filter(p => 
        p.usuario_nombre && p.usuario_nombre.toLowerCase() === nombreGuardado.toLowerCase()
      )
      if (pedidos.value.length === 0) {
        pedidos.value = response.data.filter(p => p.id_usuario === 1)
      }
    } else {
      pedidos.value = response.data.filter(p => p.id_usuario === 1)
    }

  } catch (error) {
    console.error("Error cargando perfil", error)
    usuario.value.username = localStorage.getItem('username') || 'Usuario'
  } finally {
    cargando.value = false
  }
}

onMounted(cargarDatos)

const abrirDetallePedido = (pedido) => {
  pedidoSeleccionado.value = pedido
  modalAbierto.value = true
}

const cerrarModal = () => {
  modalAbierto.value = false
  pedidoSeleccionado.value = null
}

const editarDireccion = () => {
  alert("Aquí se abrirá el componente para editar la dirección.")
}

const editarContrasena = () => {
  alert("Aquí se abrirá el componente para cambiar la contraseña.")
}

const cerrarSesion = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('isAdmin')
  window.dispatchEvent(new CustomEvent('carrito-actualizado'))
  router.push('/') 
}
</script>

<template>
  <div class="perfil-container">
    
    <div class="perfil-card">
      <h1 class="saludo">Hola, <span>{{ usuario.username }}</span> 👋</h1>
      
      <div class="datos-usuario">
        <div class="dato-fila">
          <strong>Correo:</strong>
          <span>{{ usuario.email }}</span>
        </div>
        <div class="dato-fila">
          <strong>Dirección de Envío:</strong>
          <span>{{ usuario.direccion || 'No especificada' }}</span>
        </div>
      </div>

      <div class="acciones-perfil">
        <button @click="editarContrasena" class="btn-secundario">Editar Contraseña</button>
        <button @click="editarDireccion" class="btn-secundario">Editar Dirección</button>
      </div>

      <div class="seccion-salir">
        <button @click="cerrarSesion" class="btn-salir">Cerrar Sesión</button>
      </div>
    </div>

    <div class="pedidos-section">
      <h2>Tus Pedidos</h2>
      <div v-if="cargando" class="msg-estado">Cargando tu historial...</div>
      
      <div v-else-if="pedidos.length === 0" class="msg-estado">
        No has realizado ninguna compra todavía.
      </div>
      
      <div v-else class="lista-pedidos">
        <div 
          v-for="pedido in pedidos" 
          :key="pedido.id" 
          class="pedido-item"
          @click="abrirDetallePedido(pedido)"
        >
          <div class="pedido-info">
            <span class="pedido-nombre">Pedido #{{ pedido.id }}</span>
            <span class="pedido-fecha">{{ new Date(pedido.fecha_pedido).toLocaleDateString() }}</span>
          </div>
          <div class="pedido-estado">
            <span class="pedido-precio">{{ pedido.total.toFixed(2) }}€</span>
            <span :class="['badge-estado', pedido.estado]">
              {{ pedido.estado.replace('_', ' ') }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="modalAbierto" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-content">
        <button class="close-btn" @click="cerrarModal">×</button>
        
        <h2 class="modal-titulo">Recibo del Pedido #{{ pedidoSeleccionado.id }}</h2>
        <p class="modal-subtitulo">Fecha: {{ new Date(pedidoSeleccionado.fecha_pedido).toLocaleString() }}</p>

        <div class="productos-lista">
          <div v-for="linea in pedidoSeleccionado.detalles" :key="linea.id" class="producto-fila">
            <div class="prod-textos">
              <strong>{{ linea.nombre_item }}</strong>
              <span class="prod-detalle">Cantidad: {{ linea.cantidad }} | {{ linea.precio_unitario.toFixed(2) }}€/ud</span>
            </div>
            <div class="prod-precio">{{ (linea.cantidad * linea.precio_unitario).toFixed(2) }}€</div>
          </div>
        </div>

        <div class="modal-total">
          <span>Total Pagado:</span>
          <strong>{{ pedidoSeleccionado.total.toFixed(2) }}€</strong>
        </div>
        
        <div class="modal-footer">
          <button @click="cerrarModal" class="btn-primario">Cerrar Recibo</button>
        </div>
      </div>
    </div>

  </div>
</template>
