<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const productos = ref([])
const errorMsg = ref('')

const busqueda = ref('')
const categoriaSeleccionada = ref('')

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/productos/')
    productos.value = response.data
    console.log("Productos cargados:", productos.value)
  } catch (error) {
    errorMsg.value = "Error al conectar con el servidor"
    console.error(error)
  }
})

const categoriasUnicas = computed(() => {
  const categorias = productos.value.map(p => p.categoria_nombre).filter(Boolean)
  return [...new Set(categorias)]
})

const productosFiltrados = computed(() => {
  return productos.value.filter(p => {
    const coincideBusqueda = p.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const coincideCategoria = categoriaSeleccionada.value === '' || p.categoria_nombre === categoriaSeleccionada.value
    return coincideBusqueda && coincideCategoria
  })
})

const resolverRutaImagen = (ruta) => {
  if (!ruta) return 'https://via.placeholder.com/200'
  if (ruta.startsWith('http')) return ruta
  return `http://127.0.0.1:8000/fotos/${ruta}`
}
</script>

<template>
  <main class="catalogo-main">
    
    <!-- NUEVA ESTRUCTURA: Los 3 elementos sueltos para que Flexbox los reparta -->
    <div class="header-catalogo">
      <h1 class="catalogo-titulo">🧵 Catálogo de Productos</h1>
      
      <!-- El filtro queda en el centro -->
      <select v-model="categoriaSeleccionada" class="select-categoria">
        <option value="">Todas las categorías</option>
        <option v-for="cat in categoriasUnicas" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>

      <!-- El buscador queda a la derecha -->
      <input 
        v-model="busqueda" 
        type="text" 
        placeholder="🔍 Buscar producto por nombre..." 
        class="input-busqueda"
      />
    </div>

    <div v-if="errorMsg" class="alerta-error">
      {{ errorMsg }}
    </div>

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
        <p class="producto-precio-etiqueta"><strong>{{ p.precio }}€</strong></p>
        
        <router-link :to="'/producto/' + p.id" class="btn-ver-detalles">
          Ver detalles
        </router-link>
      </div>
    </div>

    <div v-else-if="productos.length > 0 && productosFiltrados.length === 0" class="msg-estado">
      No se han encontrado productos que coincidan con tu búsqueda. 😢
    </div>

    <div v-else-if="!errorMsg" class="msg-estado">
      Cargando catálogo...
    </div>
  </main>
</template>

<style scoped>
/* Contenedor principal que reparte los 3 elementos */
.header-catalogo {
  display: flex;
  justify-content: space-between; /* Reparte: Izquierda, Centro, Derecha */
  align-items: center; 
  margin-bottom: 30px;
  flex-wrap: wrap; /* En móviles o pantallas pequeñas se adaptarán sin romperse */
  gap: 20px;
}

.catalogo-titulo {
  margin: 0;
  color: #d4a373;
  /* Flex basis evita que el título se encoja demasiado en pantallas medianas */
  flex: 1 1 auto; 
}

.select-categoria {
  padding: 10px 15px;
  border: 2px solid #ccd5ae;
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
  background-color: white;
  cursor: pointer;
  color: #283618;
  /* Mantiene el selector en el centro */
  flex: 0 1 auto; 
}

.select-categoria:focus {
  border-color: #606c38;
}

.input-busqueda {
  padding: 10px 15px;
  border: 2px solid #ccd5ae;
  border-radius: 25px;
  width: 100%;
  max-width: 280px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
  /* Empuja el input hacia la derecha */
  flex: 0 1 auto; 
}

.input-busqueda:focus {
  border-color: #606c38;
}

.producto-categoria {
  font-size: 0.85rem;
  color: #bc6c25;
  margin-top: -5px;
  margin-bottom: 10px;
  font-weight: 500;
}

.msg-estado {
  text-align: center; 
  color: #606c38; 
  padding: 40px; 
  font-size: 1.2rem;
}

.productos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.producto-card {
  background-color: #fefae0;
  border: 1px solid #e9edc9;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}

.producto-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 15px;
}

.producto-titulo {
  color: #283618;
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.producto-precio-etiqueta {
  color: #bc6c25;
  font-size: 1.2rem;
  margin-bottom: 15px;
  margin-top: auto; 
}

.btn-ver-detalles {
  background-color: transparent;
  color: #606c38;
  text-decoration: underline;
  padding: 10px;
  display: inline-block;
}

.btn-ver-detalles:hover {
  color: #283618;
}
</style>