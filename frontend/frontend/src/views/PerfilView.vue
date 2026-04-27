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
    const nombreGuardado = localStorage.getItem('username') || 'Usuario'
    usuario.value = {
      username: nombreGuardado,
      email: `${nombreGuardado.toLowerCase()}@costurasconmimo.es`,
      direccion: 'Av. de los Artesanos 45, 2ºB, Madrid'
    }

    const response = await axios.get('http://127.0.0.1:8000/api/pedidos/')
    
    // 1. Intentamos buscar por el nombre exacto (ignorando mayúsculas por si acaso)
    if (localStorage.getItem('username')) {
      pedidos.value = response.data.filter(p => 
        p.usuario_nombre && p.usuario_nombre.toLowerCase() === nombreGuardado.toLowerCase()
      )
      
      // 2. PARCHE DE PRUEBAS: Si la lista está vacía, mostramos los del "user_id = 1"
      // ya que el carrito los está guardando ahí por defecto ahora mismo.
      if (pedidos.value.length === 0) {
        pedidos.value = response.data.filter(p => p.id_usuario === 1)
      }
      
    } else {
      pedidos.value = response.data.filter(p => p.id_usuario === 1)
    }

  } catch (error) {
    console.error("Error cargando perfil", error)
  } finally {
    cargando.value = false
  }
}

onMounted(cargarDatos)

// --- FUNCIONES INTERACTIVAS ---
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

// Cerrar Sesión seguro
const cerrarSesion = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('isAdmin')
  // Forzamos a la navbar a darse cuenta de que salimos
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

<style scoped>
/* CONTENEDORES PRINCIPALES */
.perfil-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.perfil-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  border-top: 5px solid #606c38;
}

/* SECCIÓN DATOS */
.saludo { color: #283618; margin-top: 0; margin-bottom: 25px; }
.saludo span { color: #606c38; }

.datos-usuario { display: flex; flex-direction: column; gap: 15px; margin-bottom: 25px; }
.dato-fila { display: flex; justify-content: space-between; padding-bottom: 10px; border-bottom: 1px solid #eee; color: #333; }

.acciones-perfil { display: flex; gap: 15px; }
.btn-secundario { background: #fdfaf0; color: #606c38; border: 1px solid #606c38; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: all 0.2s; }
.btn-secundario:hover { background: #606c38; color: white; }

.seccion-salir { margin-top: 25px; border-top: 1px solid #eee; padding-top: 20px; }
.btn-salir { background: #d9534f; color: white; border: none; padding: 10px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; transition: background 0.2s; font-size: 1rem; }
.btn-salir:hover { background: #c9302c; }

/* SECCIÓN PEDIDOS */
.pedidos-section h2 { color: #283618; border-bottom: 2px solid #ccd5ae; padding-bottom: 10px; }
.msg-estado { background: white; padding: 20px; border-radius: 8px; text-align: center; color: #666; font-style: italic; }

.lista-pedidos { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
.pedido-item { background: white; padding: 15px 20px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid transparent; cursor: pointer; transition: border-color 0.2s, transform 0.2s; }
.pedido-item:hover { border-color: #606c38; transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.08); }

.pedido-info { display: flex; flex-direction: column; }
.pedido-nombre { font-weight: bold; color: #333; font-size: 1.1rem; }
.pedido-fecha { font-size: 0.85rem; color: #777; margin-top: 5px; }

.pedido-estado { display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }
.pedido-precio { font-size: 1.1rem; font-weight: bold; color: #bc6c25; }

/* ESTADOS DINÁMICOS */
.badge-estado { padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
.PENDIENTE { background: #fff3cd; color: #856404; }
.PAGADO { background: #d4edda; color: #155724; }
.EN_PREPARACION { background: #cce5ff; color: #004085; }
.ENVIADO { background: #e2e3e5; color: #383d41; }
.ENTREGADO { background: #d4edda; color: #155724; }
.CANCELADO { background: #f8d7da; color: #721c24; }

/* MODAL DE DETALLES */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; backdrop-filter: blur(2px); }
.modal-content { background: #fdfaf0; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.close-btn { position: absolute; top: 15px; right: 20px; background: none; border: none; font-size: 24px; cursor: pointer; color: #606c38; transition: 0.2s; }
.close-btn:hover { color: #d9534f; transform: scale(1.1); }

.modal-titulo { color: #283618; margin-top: 0; margin-bottom: 5px; border-bottom: 2px solid #ccd5ae; padding-bottom: 10px; }
.modal-subtitulo { color: #666; margin-bottom: 20px; font-size: 0.9rem; }

.productos-lista { display: flex; flex-direction: column; gap: 15px; background: white; padding: 15px; border-radius: 8px; border: 1px solid #ccd5ae; max-height: 300px; overflow-y: auto; }
.producto-fila { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #eee; padding-bottom: 10px; }
.producto-fila:last-child { border-bottom: none; padding-bottom: 0; }

.prod-textos { display: flex; flex-direction: column; }
.prod-detalle { font-size: 0.85rem; color: #888; margin-top: 3px; }
.prod-precio { font-weight: bold; color: #bc6c25; }

.modal-total { display: flex; justify-content: space-between; align-items: center; margin-top: 20px; background: #606c38; color: white; padding: 15px; border-radius: 8px; font-size: 1.1rem; }
.modal-footer { margin-top: 25px; text-align: right; }
.btn-primario { background: #bc6c25; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.2s; }
.btn-primario:hover { background: #9c581d; }
</style>