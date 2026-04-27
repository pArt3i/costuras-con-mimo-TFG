<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const productos = ref([])
const pedidos = ref([])
const cargando = ref(true)

// Control de ventanas modales
const productoEnEdicion = ref(null)
const pedidoSeleccionado = ref(null) // <-- Nuevo estado para ver detalles del pedido
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

// Lógica de Pedidos
const pedidosProcesados = computed(() => {
  let lista = [...pedidos.value]
  lista.sort((a, b) => {
    const da = new Date(a.fecha_pedido), db = new Date(b.fecha_pedido)
    return ordenReciente.value ? db - da : da - db
  })
  return lista.slice(0, 5)
})

// Estadísticas
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
    // Si el modal está abierto, también actualizamos su estado visualmente
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

// Para evitar que el click en el select (cambiar estado) abra también el modal de detalles
const abrirDetalles = (ped, event) => {
    // Si hemos hecho clic en el selector de estado, ignoramos para no abrir el modal
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

<style scoped>
/* Contenedor principal */
.admin-layout { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #fdfaf0; display: flex; flex-direction: column; z-index: 99999; }
.admin-header { background: #606c38; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
.brand { font-size: 1.2rem; font-weight: bold; }
.brand small { font-weight: normal; font-size: 0.9rem; opacity: 0.8; }
.btn-exit { color: white; text-decoration: none; border: 1px solid white; padding: 5px 15px; border-radius: 20px; font-size: 0.85rem; transition: 0.2s; }
.btn-exit:hover { background: white; color: #606c38; }

.loader { text-align: center; padding: 50px; font-size: 1.2rem; color: #606c38; }

/* Contenido Principal */
.admin-content { flex: 1; display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; padding: 20px; overflow: hidden; }
.panel { background: white; border-radius: 12px; display: flex; flex-direction: column; box-shadow: 0 4px 15px rgba(0,0,0,0.05); overflow: hidden; }
.panel-header { padding: 15px 20px; border-bottom: 1px solid #eee; background: #fafafa; }
.panel-header.flex { display: flex; justify-content: space-between; align-items: center; }
.panel-header h2 { font-size: 1.1rem; color: #283618; margin: 0; }
.hint { font-size: 0.8rem; color: #888; }
.btn-sort { background: white; border: 1px solid #ccd5ae; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 0.8rem; }

/* Efecto Clickable General */
.clickable { cursor: pointer; transition: 0.2s; }
.clickable:hover { background: #fefae0 !important; transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important; }

/* Lista Catálogo */
.catalog-list { flex: 1; overflow-y: auto; padding: 10px; }
.item-card { display: flex; align-items: center; gap: 15px; padding: 12px; border-bottom: 1px solid #f5f5f5; border-radius: 8px; }
.item-card img { width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #eee; }
.details { flex: 1; }
.details h3 { font-size: 1rem; margin: 0 0 5px; color: #333; }
.details p { margin: 0; font-size: 0.85rem; color: #666; }
.edit-icon { font-size: 0.8rem; color: #bc6c25; font-weight: bold; background: #fff1e6; padding: 5px 10px; border-radius: 15px; }

/* Lista Pedidos */
.orders-list { padding: 15px; overflow-y: auto; flex: 1; }
.no-data { text-align: center; color: #888; padding: 20px; font-size: 0.9rem; }
.order-mini-card { background: white; border: 1px solid #eee; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #ccd5ae; position: relative; }
.order-info { display: flex; justify-content: space-between; font-size: 0.85rem; color: #888; margin-bottom: 8px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
.id { font-weight: bold; color: #283618; font-size: 0.95rem; }
.total { color: #bc6c25; font-weight: bold; font-size: 1.1rem; margin: 5px 0; }
.status-box { margin-top: 10px; display: flex; align-items: center; gap: 10px; background: #fdfaf0; padding: 8px; border-radius: 8px; }
.status-box label { font-size: 0.85rem; font-weight: bold; color: #606c38; }
select { flex: 1; padding: 6px; border-radius: 5px; font-weight: bold; font-size: 0.85rem; border: 1px solid #ccd5ae; cursor: pointer; outline: none; }
.hint-click { font-size: 0.75rem; color: #bc6c25; text-align: right; margin-top: 10px; font-style: italic; opacity: 0.8; }

/* Footer */
.admin-footer { background: #ccd5ae; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
.stat { text-align: center; }
.stat .label { display: block; font-size: 0.75rem; font-weight: bold; color: #283618; text-transform: uppercase; margin-bottom: 5px; }
.stat .val { font-size: 1.4rem; font-weight: bold; color: #283618; }
.highlight .val { color: #bc6c25; font-size: 1.6rem; }

/* Modales */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 100000; }
.modal-card { background: white; padding: 30px; border-radius: 15px; width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); max-height: 90vh; display: flex; flex-direction: column; }
.modal-larga { width: 500px; }

/* Estilos específicos del Modal de Pedidos */
.modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 15px; }
.modal-header h3 { margin: 0; color: #283618; }
.btn-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #888; }
.info-cliente { background: #fdfaf0; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9rem; }
.info-cliente p { margin: 5px 0; }
.badge-estado { background: #ccd5ae; color: #283618; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }
.subtitulo { color: #bc6c25; margin-bottom: 10px; font-size: 1.1rem; }

.lista-articulos { overflow-y: auto; flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 10px; margin-bottom: 20px; }
.articulo-linea { display: flex; align-items: center; gap: 15px; padding: 10px 0; border-bottom: 1px solid #f5f5f5; }
.articulo-linea:last-child { border-bottom: none; }
.mini-img { width: 40px; height: 40px; object-fit: cover; border-radius: 5px; }
.mini-img-placeholder { width: 40px; height: 40px; background: #eee; display: flex; justify-content: center; align-items: center; border-radius: 5px; font-size: 1.5rem; }
.art-info { flex: 1; }
.art-info strong { display: block; font-size: 0.95rem; color: #333; }
.cantidad { font-size: 0.8rem; color: #666; margin: 3px 0 0; }
.art-precio { font-weight: bold; color: #283618; }

.total-pedido { display: flex; justify-content: space-between; align-items: center; font-size: 1.2rem; background: #606c38; color: white; padding: 15px; border-radius: 8px; }

/* Estilos de inputs (para Modal de edición) */
.row { display: flex; gap: 15px; }
.input-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 5px; flex: 1; }
.input-group label { font-size: 0.85rem; font-weight: bold; color: #606c38; }
.input-group input { padding: 10px; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; }
.modal-actions { display: flex; gap: 10px; margin-top: 10px; }
.btn-save { flex: 1; background: #606c38; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.2s; }
.btn-save:hover { background: #4a532a; }
.btn-cancel { flex: 1; background: #eee; color: #555; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.2s; }
</style>