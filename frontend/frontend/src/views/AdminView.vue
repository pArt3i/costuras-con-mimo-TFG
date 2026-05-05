<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const productos = ref([])
const pedidos = ref([])
const tejidos = ref([])
const categorias = ref([])
const cargando = ref(true)

// Control de ventanas modales
const productoEnEdicion = ref(null)
const tejidoEnEdicion = ref(null)
const pedidoSeleccionado = ref(null)

const ordenReciente = ref(true)

// Variables reactivas para los filtros
const filtroCategoriaProducto = ref('')
const filtroArtista = ref('')
const filtroUsuario = ref('')
const filtroPedidoId = ref('')

// --- FUNCIÓN DE SEGURIDAD PARA MANDAR EL TOKEN ---
const getAuthHeaders = () => {
  const token = localStorage.getItem('token')
  return token ? { headers: { Authorization: `Bearer ${token}` } } : {}
}

const cargarDatos = async () => {
  try {
    const [resP, resO, resT, resC] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/productos/', getAuthHeaders()),
      axios.get('http://127.0.0.1:8000/api/pedidos/', getAuthHeaders()),
      axios.get('http://127.0.0.1:8000/api/tejidos/', getAuthHeaders()),
      axios.get('http://127.0.0.1:8000/api/categorias/', getAuthHeaders())
    ])
    
    productos.value = Array.isArray(resP.data) ? resP.data : (resP.data.results || [])
    pedidos.value = Array.isArray(resO.data) ? resO.data : (resO.data.results || [])
    tejidos.value = Array.isArray(resT.data) ? resT.data : (resT.data.results || [])
    categorias.value = Array.isArray(resC.data) ? resC.data : (resC.data.results || [])

  } catch (e) {
    console.error("Error cargando el dashboard:", e)
    productos.value = []
    pedidos.value = []
    tejidos.value = []
    categorias.value = []
  } finally {
    cargando.value = false
  }
}

// Lógica computada para aplicar filtros a los Productos
const productosProcesados = computed(() => {
  if (!Array.isArray(productos.value)) return []
  
  return productos.value.filter(p => {
    // Filtro por Categoría
    const matchCat = filtroCategoriaProducto.value === '' || p.id_categoria == filtroCategoriaProducto.value
    // Filtro por Artista (Preparado para cuando actualices la base de datos)
    const matchArtista = filtroArtista.value === '' || (p.artista && p.artista.toLowerCase().includes(filtroArtista.value.toLowerCase()))
    
    return matchCat && matchArtista
  })
})

// Lógica computada para aplicar filtros a los Pedidos
const pedidosProcesados = computed(() => {
  if (!Array.isArray(pedidos.value)) return []
  
  let lista = pedidos.value.filter(ped => {
    // Filtro por Cliente
    const matchUsuario = filtroUsuario.value === '' || (ped.usuario_nombre && ped.usuario_nombre.toLowerCase().includes(filtroUsuario.value.toLowerCase()))
    // Filtro por ID de Pedido
    const matchId = filtroPedidoId.value === '' || ped.id.toString() === filtroPedidoId.value.toString()
    
    return matchUsuario && matchId
  })

  // Ordenar después de filtrar
  lista.sort((a, b) => {
    const da = new Date(a.fecha_pedido), db = new Date(b.fecha_pedido)
    return ordenReciente.value ? db - da : da - db
  })
  return lista
})

const stats = computed(() => {
  if (!Array.isArray(pedidos.value)) return { totalPedidos: 0, ventas: "0.00" }
  
  const ventasTotales = pedidos.value.reduce((acc, pedido) => acc + (pedido.total || 0), 0)
  return {
    totalPedidos: pedidos.value.length,
    ventas: ventasTotales.toFixed(2)
  }
})

const cambiarEstadoPedido = async (id, nuevoEstado) => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/pedidos/${id}/`, { estado: nuevoEstado }, getAuthHeaders())
    alert(`Estado del pedido #${id} actualizado a ${nuevoEstado}`)
    cargarDatos()
    if(pedidoSeleccionado.value && pedidoSeleccionado.value.id === id) {
        pedidoSeleccionado.value.estado = nuevoEstado
    }
  } catch (e) { 
    console.error(e)
    alert("Error al actualizar estado") 
  }
}

// --- LÓGICA DE PRODUCTOS Y TEJIDOS ---
const nuevoProducto = () => {
  // Cuando actualices la BD, añade 'artista: ""' aquí también si es necesario editarlo manual
  productoEnEdicion.value = { nombre: '', precio: 0, stock: 0, img: '', id_categoria: '' }
}

const guardarCambiosProducto = async () => {
  try {
    if (productoEnEdicion.value.id) {
      await axios.patch(`http://127.0.0.1:8000/api/productos/${productoEnEdicion.value.id}/`, productoEnEdicion.value, getAuthHeaders())
      alert("Producto modificado correctamente")
    } else {
      await axios.post(`http://127.0.0.1:8000/api/productos/`, productoEnEdicion.value, getAuthHeaders())
      alert("Producto creado correctamente")
    }
    productoEnEdicion.value = null
    cargarDatos()
  } catch (e) { 
    console.error(e)
    alert("Error al guardar el producto. Revisa los datos.") 
  }
}

const nuevoTejido = () => {
  tejidoEnEdicion.value = { nombre_tej: '', img: '' }
}

const guardarCambiosTejido = async () => {
  try {
    if (tejidoEnEdicion.value.id) {
      await axios.patch(`http://127.0.0.1:8000/api/tejidos/${tejidoEnEdicion.value.id}/`, tejidoEnEdicion.value, getAuthHeaders())
      alert("Tejido modificado correctamente")
    } else {
      await axios.post(`http://127.0.0.1:8000/api/tejidos/`, tejidoEnEdicion.value, getAuthHeaders())
      alert("Tejido añadido al taller correctamente")
    }
    tejidoEnEdicion.value = null
    cargarDatos()
  } catch (e) { 
    console.error(e)
    alert("Error al guardar el tejido.") 
  }
}

const abrirDetalles = (ped, event) => {
    if (event.target.tagName === 'SELECT') return;
    pedidoSeleccionado.value = ped;
}

const getImg = (imgUrl) => {
  if (!imgUrl) return 'https://placehold.co/150x150/e9edc9/606c38?text=Sin+Foto'
  return imgUrl.startsWith('http') ? imgUrl : `http://127.0.0.1:8000/fotos/${imgUrl}`
}

onMounted(cargarDatos)
</script>

<template>
  <div class="admin-layout-fondo">
    <div class="admin-layout">
      <header class="admin-header">
        <div class="brand">🧶 Costuras con Mimo <small>| Panel de Control</small></div>
        <router-link to="/" class="btn-exit">Volver a la Tienda</router-link>
      </header>

      <div v-if="cargando" class="loader">Conectando con el taller...</div>

      <main v-else class="admin-content dos-columnas">
        
        <!-- COLUMNA IZQUIERDA (Productos y Tejidos) -->
        <div class="columna-izquierda">
          <!-- SECCIÓN 1: PRODUCTOS -->
          <section class="panel panel-catalog">
            <div class="panel-header flex-columna">
              <div class="cabecera-principal flex">
                <div>
                  <h2>📦 Inventario de Productos</h2>
                  <span class="hint">Haz clic para editar, o crea uno nuevo</span>
                </div>
                <button @click="nuevoProducto" class="btn-add">+ Añadir Producto</button>
              </div>
              
              <!-- ZONA DE FILTROS PRODUCTOS -->
              <div class="filtros-container">
                <select v-model="filtroCategoriaProducto" class="input-filtro">
                  <option value="">Todas las categorías</option>
                  <option v-for="cat in categorias" :key="cat.id" :value="cat.id">{{ cat.nombre_cat }}</option>
                </select>
                <input type="text" v-model="filtroArtista" placeholder="Filtrar por artista..." class="input-filtro">
              </div>
            </div>

            <div class="catalog-list scrollable-list">
              <div v-if="productosProcesados.length === 0" class="no-data">No hay productos que coincidan.</div>
              <div v-for="p in productosProcesados" :key="p.id" class="item-card clickable" @click="productoEnEdicion = {...p}">
                <img :src="getImg(p.img)">
                <div class="details">
                  <h3>{{ p.nombre }}</h3>
                  <p>Precio: <strong>{{ p.precio }}€</strong> | Stock: <strong>{{ p.stock }}</strong></p>
                  <p v-if="p.artista" style="font-size: 0.8rem; color: #606c38;">🎨 {{ p.artista }}</p>
                </div>
                <div class="edit-icon">✏️ Editar</div>
              </div>
            </div>
          </section>

          <!-- SECCIÓN 2: TEJIDOS -->
          <section class="panel panel-catalog">
            <div class="panel-header flex">
              <div>
                <h2>🧵 Telas y Estampados</h2>
                <span class="hint">Materiales disponibles para personalizar</span>
              </div>
              <button @click="nuevoTejido" class="btn-add">+ Añadir Tejido</button>
            </div>
            <div class="catalog-list scrollable-list">
              <div v-for="t in tejidos" :key="t.id" class="item-card clickable" @click="tejidoEnEdicion = {...t}">
                <img :src="getImg(t.img)">
                <div class="details">
                  <h3>{{ t.nombre_tej }}</h3>
                </div>
                <div class="edit-icon">✏️ Editar</div>
              </div>
            </div>
          </section>
        </div>

        <!-- COLUMNA DERECHA (Pedidos) -->
        <div class="columna-derecha">
          <section class="panel panel-orders panel-completo">
            <div class="panel-header flex-columna">
              <div class="cabecera-principal flex">
                <h2>🛒 Últimos Pedidos</h2>
                <button @click="ordenReciente = !ordenReciente" class="btn-sort">
                  {{ ordenReciente ? '📅 Ver Antiguos' : '📅 Ver Recientes' }}
                </button>
              </div>

              <!-- ZONA DE FILTROS PEDIDOS -->
              <div class="filtros-container">
                <input type="number" v-model="filtroPedidoId" placeholder="Nº de pedido..." class="input-filtro input-corto">
                <input type="text" v-model="filtroUsuario" placeholder="Buscar por cliente..." class="input-filtro">
              </div>
            </div>
            
            <div class="orders-list scrollable-list">
              <div v-if="pedidosProcesados.length === 0" class="no-data">No hay pedidos que coincidan con la búsqueda.</div>
              
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
        </div>
        
      </main>

      <footer class="admin-footer">
        <div class="stat">
          <span class="label">Total Tejidos</span>
          <span class="val">{{ tejidos.length }}</span>
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

      <!-- (Modales de Producto, Tejido y Pedido se mantienen intactos en la plantilla base) -->
      <!-- ... -->
      <div v-if="productoEnEdicion" class="modal-overlay" @click.self="productoEnEdicion = null">
        <!-- Contenido Modal Producto -->
        <div class="modal-card">
          <h3>{{ productoEnEdicion.id ? 'Modificar Producto' : 'Crear Nuevo Producto' }}</h3>
          <div class="input-group">
            <label>Nombre del Producto:</label>
            <input v-model="productoEnEdicion.nombre" type="text" placeholder="Ej. Mochila Guardería">
          </div>
          <!-- Nuevo input de Artista (Opcional por ahora) -->
          <div class="input-group">
            <label>Artista (Opcional):</label>
            <input v-model="productoEnEdicion.artista" type="text" placeholder="Nombre del artesano">
          </div>
          <div class="input-group">
            <label>Categoría:</label>
            <select v-model="productoEnEdicion.id_categoria">
              <option value="" disabled>Selecciona una categoría</option>
              <option v-for="cat in categorias" :key="cat.id" :value="cat.id">{{ cat.nombre_cat }}</option>
            </select>
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
          <div class="input-group">
            <label>Nombre del archivo de imagen:</label>
            <input v-model="productoEnEdicion.img" type="text" placeholder="ejemplo.png o URL completa">
          </div>
          <div class="modal-actions">
            <button @click="guardarCambiosProducto" class="btn-save">{{ productoEnEdicion.id ? 'Guardar Cambios' : 'Crear Producto' }}</button>
            <button @click="productoEnEdicion = null" class="btn-cancel">Cancelar</button>
          </div>
        </div>
      </div>

      <!-- MODAL TEJIDO -->
      <div v-if="tejidoEnEdicion" class="modal-overlay" @click.self="tejidoEnEdicion = null">
        <div class="modal-card">
          <h3>{{ tejidoEnEdicion.id ? 'Modificar Tejido' : 'Añadir Nuevo Tejido' }}</h3>
          
          <div class="input-group">
            <label>Nombre de la Tela/Estampado:</label>
            <input v-model="tejidoEnEdicion.nombre_tej" type="text" placeholder="Ej. Algodón Estrellas">
          </div>

          <div class="input-group">
            <label>Nombre del archivo de imagen:</label>
            <input v-model="tejidoEnEdicion.img" type="text" placeholder="tela1.png o URL completa">
          </div>

          <div class="modal-actions">
            <button @click="guardarCambiosTejido" class="btn-save">{{ tejidoEnEdicion.id ? 'Guardar Cambios' : 'Añadir Tejido' }}</button>
            <button @click="tejidoEnEdicion = null" class="btn-cancel">Cancelar</button>
          </div>
        </div>
      </div>

      <!-- MODAL RECIBO PEDIDO -->
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
              <div v-if="pedidoSeleccionado.detalles && pedidoSeleccionado.detalles.length === 0" class="no-data">No hay detalles registrados.</div>
              
              <div v-for="linea in (pedidoSeleccionado.detalles || [])" :key="linea.id" class="articulo-linea">
                  <img v-if="linea.imagen_item" :src="getImg(linea.imagen_item)" class="mini-img">
                  <div v-else class="mini-img-placeholder">🎨</div>
                  
                  <div class="art-info">
                      <strong>{{ linea.nombre_item }}</strong>
                      <p class="cantidad">Cantidad: {{ linea.cantidad }} | {{ (linea.precio_unitario || 0).toFixed(2) }}€ / ud</p>
                  </div>
                  <div class="art-precio">
                      {{ ((linea.cantidad || 0) * (linea.precio_unitario || 0)).toFixed(2) }}€
                  </div>
              </div>
          </div>

          <div class="total-pedido">
              <span>Total del Pedido:</span>
              <strong>{{ (pedidoSeleccionado.total || 0).toFixed(2) }}€</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* =========================================================
   ESTILOS PARA FONDO, PANELES Y SCROLL
   ========================================================= */

/* Creamos un div extra para asegurar que el fondo se extienda en toda la vista */
.admin-layout-fondo {
  background-color: #e9edc9; /* Color de fondo general claro */
  min-height: 100vh;
  padding: 10px 0; /* Un poco de respiro si lo necesitas */
}

.admin-layout {
  /* Mantenemos tu layout pero nos aseguramos de que no choque con el fondo */
  max-width: 1400px;
  margin: 0 auto;
}

/* Forzamos que cada panel sea blanco puro con una sombra suave para resaltar */
.panel {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); 
  padding: 20px;
}

.dos-columnas {
  display: flex;
  gap: 30px;
  padding: 0 20px; /* Separación horizontal del borde de la pantalla */
}

.columna-izquierda {
  flex: 2; 
  display: flex;
  flex-direction: column;
  gap: 30px;
  height: calc(100vh - 220px); 
}

.columna-derecha {
  flex: 1; 
  height: calc(100vh - 220px); 
}

.panel-catalog {
  flex: 1; 
  display: flex;
  flex-direction: column;
}

.panel-completo {
  height: 100%; 
  display: flex;
  flex-direction: column;
}

.panel-header.flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px; 
}

/* Modificaciones para integrar los filtros */
.panel-header.flex-columna {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f4f5f0;
  margin-bottom: 10px;
}

.cabecera-principal.flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.filtros-container {
  display: flex;
  gap: 10px;
  width: 100%;
}

.input-filtro {
  padding: 8px 12px;
  border: 1px solid #ccd5ae;
  border-radius: 5px;
  font-size: 0.9rem;
  outline: none;
  flex: 1;
  background-color: #fefae0;
  color: #283618;
}

.input-filtro:focus {
  border-color: #606c38;
}

.input-corto {
  flex: 0.4; /* Hace que el campo del ID de pedido sea más pequeño que el del nombre */
}

.scrollable-list {
  flex: 1; 
  overflow-y: auto;
  padding-right: 10px;
  min-height: 0; 
}

.scrollable-list::-webkit-scrollbar {
  width: 6px;
}
.scrollable-list::-webkit-scrollbar-thumb {
  background: #ccd5ae;
  border-radius: 4px;
}
.scrollable-list::-webkit-scrollbar-track {
  background: transparent; 
}

.btn-add {
  background-color: #bc6c25;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: #a05a1d;
}

@media (max-width: 900px) {
  .dos-columnas {
    flex-direction: column;
  }
  .columna-izquierda, .columna-derecha {
    width: 100%;
    height: auto; 
  }
  .panel-completo, .panel-catalog {
    height: auto;
  }
  .scrollable-list {
    max-height: 45vh; 
  }
}
</style>