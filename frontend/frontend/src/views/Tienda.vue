<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const productos = ref([])
const artistas = ref([]) // Nueva lista para los administradores/artistas
const errorMsg = ref('')

// Variables reactivas para los filtros y búsqueda
const busqueda = ref('')
const categoriaSeleccionada = ref('')
const artistaSeleccionado = ref('')

// Dos variables de ordenación independientes
const ordenFecha = ref('recientes') // Por defecto enseñamos los más nuevos
const ordenPrecio = ref('') // Por defecto sin orden de precio específico

onMounted(async () => {
  try {
    // Pedimos los productos
    const resProductos = await axios.get('http://127.0.0.1:8000/api/productos/')
    productos.value = resProductos.data
    
    // Pedimos los usuarios para sacar a los administradores (artistas)
    try {
      const resUsuarios = await axios.get('http://127.0.0.1:8000/api/usuarios/')
      const listaUsuarios = Array.isArray(resUsuarios.data) ? resUsuarios.data : (resUsuarios.data.results || [])
      // Filtramos solo los que son superuser y nos quedamos con su username
      artistas.value = listaUsuarios.filter(u => u.is_superuser).map(u => u.username)
    } catch (errUser) {
      console.warn("No se pudo cargar la lista de usuarios. Verifica los permisos en Django.", errUser)
      // Plan B (por si falla la API de usuarios): sacamos los artistas de los propios productos
      const artistasEnProductos = productos.value.map(p => p.artista).filter(Boolean)
      artistas.value = [...new Set(artistasEnProductos)]
    }

  } catch (error) {
    errorMsg.value = "Error al conectar con el servidor"
    console.error(error)
  }
})

// Extraemos categorías únicas que existan en los productos
const categoriasUnicas = computed(() => {
  const categorias = productos.value.map(p => p.categoria_nombre).filter(Boolean)
  return [...new Set(categorias)]
})

// Lógica principal: Filtra y luego aplica DOBLE ORDENACIÓN
const productosFiltrados = computed(() => {
  // 1. Aplicamos los filtros de texto y desplegables
  let lista = productos.value.filter(p => {
    const coincideBusqueda = p.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const coincideCategoria = categoriaSeleccionada.value === '' || p.categoria_nombre === categoriaSeleccionada.value
    const coincideArtista = artistaSeleccionado.value === '' || 
      (p.artista && p.artista.toLowerCase() === artistaSeleccionado.value.toLowerCase())
    
    return coincideBusqueda && coincideCategoria && coincideArtista
  })

  // 2. Aplicamos la ordenación doble
  lista.sort((a, b) => {
    // --- PRIMERO ORDENAMOS POR PRECIO (Si el usuario ha elegido uno) ---
    if (ordenPrecio.value === 'asc') {
      const diffPrecio = parseFloat(a.precio) - parseFloat(b.precio)
      if (diffPrecio !== 0) return diffPrecio 
    } 
    else if (ordenPrecio.value === 'desc') {
      const diffPrecio = parseFloat(b.precio) - parseFloat(a.precio)
      if (diffPrecio !== 0) return diffPrecio
    }

    // --- SEGUNDO ORDENAMOS POR FECHA (Si los precios son iguales o no hay orden de precio) ---
    const fechaA = a.fecha_creacion ? new Date(a.fecha_creacion) : new Date(0)
    const fechaB = b.fecha_creacion ? new Date(b.fecha_creacion) : new Date(0)
    
    if (ordenFecha.value === 'antiguos') {
      return fechaA - fechaB
    } else { 
      // Por defecto siempre es 'recientes'
      return fechaB - fechaA
    }
  })

  return lista
})

const resolverRutaImagen = (ruta) => {
  if (!ruta) return 'https://placehold.co/200x200/e9edc9/606c38?text=Sin+Foto'
  if (ruta.startsWith('http')) return ruta
  return `http://127.0.0.1:8000/fotos/${ruta}`
}
</script>

<template>
  <main class="catalogo-main">
    
    <!-- CABECERA: Título -->
    <div class="header-catalogo">
      <h1 class="catalogo-titulo">🧵 Catálogo del Taller</h1>
    </div>

    <!-- BARRA DE FILTROS SECUNDARIA (Filtros - Buscador - Orden) -->
    <div class="barra-filtros">
      
      <!-- IZQUIERDA: Filtros -->
      <div class="grupo-filtros">
        <!-- Filtro Categoría -->
        <div class="orden-item">
          <label class="label-orden">Categoría:</label>
          <select v-model="categoriaSeleccionada" class="select-filtro select-orden">
            <option value="">Todas</option>
            <option v-for="cat in categoriasUnicas" :key="cat" :value="cat">
              {{ cat }}
            </option>
          </select>
        </div>

        <!-- Filtro Artista -->
        <div class="orden-item">
          <label class="label-orden">Artesano:</label>
          <select v-model="artistaSeleccionado" class="select-filtro select-orden">
            <option value="">Todos</option>
            <option v-for="artista in artistas" :key="artista" :value="artista">
              🎨 {{ artista }}
            </option>
          </select>
        </div>
      </div>

      <!-- CENTRO: Buscador -->
      <div class="grupo-buscador">
        <input 
          v-model="busqueda" 
          type="text" 
          placeholder="🔍 Buscar producto por nombre..." 
          class="input-busqueda"
        />
      </div>

      <!-- DERECHA: Selectores de Ordenación -->
      <div class="grupo-orden">
        <!-- Orden por Precio -->
        <div class="orden-item">
          <label class="label-orden">Precio:</label>
          <select v-model="ordenPrecio" class="select-filtro select-orden">
            <option value="">Cualquiera</option>
            <option value="asc">Menor a mayor</option>
            <option value="desc">Mayor a menor</option>
          </select>
        </div>

        <!-- Orden por Fecha -->
        <div class="orden-item">
          <label class="label-orden">Fecha:</label>
          <select v-model="ordenFecha" class="select-filtro select-orden">
            <option value="recientes">Más recientes</option>
            <option value="antiguos">Más antiguos</option>
          </select>
        </div>
      </div>
      
    </div>

    <!-- Mensajes de Error y Estado -->
    <div v-if="errorMsg" class="alerta-error">
      {{ errorMsg }}
    </div>

    <!-- Grid de Productos -->
    <div v-if="productosFiltrados.length > 0" class="productos-grid">
      <div v-for="p in productosFiltrados" :key="p.id" class="producto-card">
        <img 
          :src="resolverRutaImagen(p.img)" 
          :alt="p.nombre" 
          @error="(e) => console.error('Error cargando imagen:', e.target.src)"
          class="producto-img"
        />
        <h3 class="producto-titulo">{{ p.nombre }}</h3>
        <p class="producto-categoria" v-if="p.categoria_nombre">{{ p.categoria_nombre }}</p>
        <p class="producto-artista" v-if="p.artista">Artesano: <strong>{{ p.artista }}</strong></p>
        <p class="producto-precio-etiqueta"><strong>{{ p.precio }}€</strong></p>
        <router-link :to="'/producto/' + p.id" class="btn-ver-detalles">
          Ver detalles
        </router-link>
      </div>
    </div>

    <div v-else-if="productos.length > 0 && productosFiltrados.length === 0" class="msg-estado">
      No se han encontrado productos con esos filtros. 😢
    </div>

    <div v-else-if="!errorMsg" class="msg-estado">
      Cargando catálogo...
    </div>
  </main>
</template>