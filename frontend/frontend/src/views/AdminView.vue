<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const productos = ref([])
const pedidos = ref([])
const cargando = ref(true)

const productoEnEdicion = ref(null)
const pedidoSeleccionado = ref(null)
const ordenReciente = ref(true)

const cargarDatos = async () => {
  try {
    const [resP, resO] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/productos/'),
      axios.get('http://127.0.0.1:8000/api/pedidos/')
    ])
    productos.value = resP.data
    pedidos.value = resO.data
  } catch (e) {
    console.error("Error cargando el dashboard:", e)
  } finally {
    cargando.value = false
  }
}

const pedidosProcesados = computed(() => {
  let lista = [...pedidos.value]
  lista.sort((a, b) => {
    const da = new Date(a.fecha_pedido), db = new Date(b.fecha_pedido)
    return ordenReciente.value ? db - da : da - db
  })
  return lista.slice(0, 5)
})

const stats = computed(() => {
  const ventasTotales = pedidos.value.reduce((acc, pedido) => acc + pedido.total, 0)
  return {
    totalPedidos: pedidos.value.length,
    ventas: ventasTotales.toFixed(2)
  }
})

const cambiarEstadoPedido = async (id, nuevoEstado) => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/pedidos/${id}/`, { estado: nuevoEstado })
    alert(`Estado del pedido #${id} actualizado a ${nuevoEstado}`)
    cargarDatos()
    if(pedidoSeleccionado.value && pedidoSeleccionado.value.id === id) {
        pedidoSeleccionado.value.estado = nuevoEstado
    }
  } catch (e) { 
    alert("Error al actualizar estado") 
  }
}

const guardarCambiosProducto = async () => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/productos/${productoEnEdicion.value.id}/`, productoEnEdicion.value)
    alert("Producto modificado correctamente")
    productoEnEdicion.value = null
    cargarDatos()
  } catch (e) { 
    alert("Error al modificar producto") 
  }
}

const abrirDetalles = (ped, event) => {
    if (event.target.tagName === 'SELECT') return;
    pedidoSeleccionado.value = ped;
}

onMounted(cargarDatos)
</script>

<template>
  <div class="admin-layout">
    <header class="admin-header">
      <div class="brand">🧶 Costuras con Mimo <small>| Panel de Control</small></div>
      <router-link to="/" class="btn-exit">Volver a la Tienda</router-link>
    </header>

    <div v-if="cargando" class="loader">Conectando con el taller...</div>

    <main v-else class="admin-content">
      <section class="panel panel-catalog">
        <div class="panel-header">
          <h2>📦 Inventario en Venta</h2>
          <span class="hint">Haz clic en un producto para modificarlo</span>
        </div>
        <div class="catalog-list">
          <div v-for="p in productos" :key="p.id" class="item-card clickable" @click="productoEnEdicion = {...p}">
            <img :src="p.img.startsWith('http') ? p.img : 'http://127.0.0.1:8000/fotos/'+p.img">
            <div class="details">
              <h3>{{ p.nombre }}</h3>
              <p>Precio: <strong>{{ p.precio }}€</strong> | Stock: <strong>{{ p.stock }}</strong></p>
            </div>
            <div class="edit-icon">✏️ Editar</div>
          </div>
        </div>
      </section>

      <section class="panel panel-orders">
        <div class="panel-header flex">
          <h2>🛒 Últimos Pedidos</h2>
          <button @click="ordenReciente = !ordenReciente" class="btn-sort">
            {{ ordenReciente ? '📅 Ver Antiguos' : '📅 Ver Recientes' }}
          </button>
        </div>
        <div class="orders-list">
          <div v-if="pedidosProcesados.length === 0" class="no-data">No hay pedidos registrados.</div>
          
          <div v-for="ped in pedidosProcesados" :key="ped.id" class="order-mini-card clickable" @click="abrirDetalles(ped, $event)">
            <div class="order-info">
              <span class="id">#{{ ped.id }}</span>
              <span class="date">{{ new Date(ped.fecha_pedido).toLocaleDateString() }}</span>
            </div>
            <p>Cliente: <strong>{{ ped.usuario_nombre }}</strong></p>
            <p class="total">Total: {{ ped.total.toFixed(2) }}€</p>
            
            <div class="status-box">
              <label>Estado:</label>
              <select :value="ped.estado" @change="cambiarEstadoPedido(ped.id, $event.target.value)">
                <option value="PENDIENTE">Pendiente</option>
                <option value="PAGADO">Pagado</option>
                <option value="EN_PREPARACION">En Preparación</option>
                <option value="ENVIADO">Enviado</option>
                <option value="ENTREGADO">Entregado</option>
                <option value="CANCELADO">Cancelado</option>
              </select>
            </div>
            <div class="hint-click">Haz clic para ver qué contiene 📦</div>
          </div>
        </div>
      </section>
    </main>

    <footer class="admin-footer">
      <div class="stat">
        <span class="label">Usuarios Registrados</span>
        <span class="val">--</span>
      </div>
      <div class="stat">
        <span class="label">Pedidos Totales</span>
        <span class="val">{{ stats.totalPedidos }}</span>
      </div>
      <div class="stat highlight">
        <span class="label">Facturación Total</span>
        <span class="val">{{ stats.ventas }}€</span>
      </div>
    </footer>

    <div v-if="productoEnEdicion" class="modal-overlay" @click.self="productoEnEdicion = null">
      <div class="modal-card">
        <h3>Modificar Producto</h3>
        <div class="input-group">
          <label>Nombre del Producto:</label>
          <input v-model="productoEnEdicion.nombre" type="text">
        </div>
        <div class="row">
          <div class="input-group">
            <label>Precio (€):</label>
            <input type="number" step="0.01" v-model="productoEnEdicion.precio">
          </div>
          <div class="input-group">
            <label>Unidades en Stock:</label>
            <input type="number" v-model="productoEnEdicion.stock">
          </div>
        </div>
        <div class="modal-actions">
          <button @click="guardarCambiosProducto" class="btn-save">Guardar Cambios</button>
          <button @click="productoEnEdicion = null" class="btn-cancel">Cancelar</button>
        </div>
      </div>
    </div>

    <div v-if="pedidoSeleccionado" class="modal-overlay" @click.self="pedidoSeleccionado = null">
      <div class="modal-card modal-larga">
        <div class="modal-header">
            <h3>Recibo del Pedido #{{ pedidoSeleccionado.id }}</h3>
            <button @click="pedidoSeleccionado = null" class="btn-close">×</button>
        </div>
        
        <div class="info-cliente">
            <p><strong>Cliente:</strong> {{ pedidoSeleccionado.usuario_nombre }}</p>
            <p><strong>Fecha:</strong> {{ new Date(pedidoSeleccionado.fecha_pedido).toLocaleString() }}</p>
            <p><strong>Estado:</strong> <span class="badge-estado">{{ pedidoSeleccionado.estado }}</span></p>
        </div>

        <h4 class="subtitulo">Artículos a preparar:</h4>
        <div class="lista-articulos">
            <div v-if="pedidoSeleccionado.detalles.length === 0" class="no-data">No hay detalles registrados.</div>
            
            <div v-for="linea in pedidoSeleccionado.detalles" :key="linea.id" class="articulo-linea">
                <img v-if="linea.imagen_item" :src="linea.imagen_item.startsWith('http') ? linea.imagen_item : 'http://127.0.0.1:8000/fotos/'+linea.imagen_item" class="mini-img">
                <div v-else class="mini-img-placeholder">🎨</div>
                
                <div class="art-info">
                    <strong>{{ linea.nombre_item }}</strong>
                    <p class="cantidad">Cantidad: {{ linea.cantidad }} | {{ linea.precio_unitario.toFixed(2) }}€ / ud</p>
                </div>
                <div class="art-precio">
                    {{ (linea.cantidad * linea.precio_unitario).toFixed(2) }}€
                </div>
            </div>
        </div>

        <div class="total-pedido">
            <span>Total del Pedido:</span>
            <strong>{{ pedidoSeleccionado.total.toFixed(2) }}€</strong>
        </div>
      </div>
    </div>

  </div>
</template>
