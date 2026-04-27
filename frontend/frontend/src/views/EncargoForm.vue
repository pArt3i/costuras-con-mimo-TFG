<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const tejidos = ref([])
const cargando = ref(false)

// Precios base para encargos personalizados
const preciosBase = {
  'Mochila Personalizada': 45.0,
  'Babero Personalizado': 18.0,
  'Cambiador Personalizado': 28.0
}

const formulario = ref({
  id_usuario: 1, // Nota: Más adelante lo sacaremos del usuario logueado
  id_producto: null, // Sigue siendo null porque es un ENCARGO, no un producto de catálogo
  producto_type: 'Mochila Personalizada',
  id_tejido: '',
  bordado: '',
  precio: 45.0,
  estado: 'CARRITO'
})

onMounted(async () => {
  try {
    // Cargamos los tejidos reales que has metido en Django
    const resTejidos = await axios.get('http://127.0.0.1:8000/api/tejidos/')
    tejidos.value = resTejidos.data
  } catch (error) {
    console.error("Error al cargar tejidos:", error)
  }
})

const actualizarPrecio = () => {
  formulario.value.precio = preciosBase[formulario.value.producto_type]
}

const añadirAlCarrito = async () => {
  if (!formulario.value.id_tejido) {
    alert("Por favor, selecciona una tela.");
    return;
  }

  cargando.value = true
  try {
    // Enviamos el encargo personalizado a la tabla Encargos de Django
    await axios.post('http://127.0.0.1:8000/api/encargos/', formulario.value)
    
    // Avisamos a la Navbar para que actualice el contador
    window.dispatchEvent(new CustomEvent('carrito-actualizado'))
    
    alert("¡Tu encargo personalizado se ha añadido a la cesta!")
    router.push('/carrito')
  } catch (error) {
    console.error("Error al guardar el encargo:", error)
    alert("Hubo un error al guardar tu personalización.")
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="container">
    <div class="encargo-card">
      <h1>✨ Diseña tu Encargo</h1>
      <p class="subtitulo">Elige el producto, la tela y dinos qué nombre bordamos.</p>

      <form @submit.prevent="añadirAlCarrito" class="form-personalizar">
        
        <div class="campo">
          <label>¿Qué artículo quieres personalizar?</label>
          <select v-model="formulario.producto_type" @change="actualizarPrecio">
            <option v-for="(precio, tipo) in preciosBase" :key="tipo" :value="tipo">
              {{ tipo }} ({{ precio }}€)
            </option>
          </select>
        </div>

        <div class="campo">
          <label>Selecciona tu tela favorita:</label>
          <div class="tejidos-grid">
            <label v-for="t in tejidos" :key="t.id" class="tejido-item" :class="{ seleccionado: formulario.id_tejido === t.id }">
              <input type="radio" :value="t.id" v-model="formulario.id_tejido" name="tejido" required>
              <img :src="t.img.startsWith('http') ? t.img : 'http://127.0.0.1:8000/fotos/' + t.img" :alt="t.nombre_tej">
              <span>{{ t.nombre_tej }}</span>
            </label>
          </div>
        </div>

        <div class="campo">
          <label>Nombre o texto a bordar:</label>
          <input 
            type="text" 
            v-model="formulario.bordado" 
            placeholder="Ej: Sofía o Pablo" 
            maxlength="20"
            required
          >
        </div>

        <div class="resumen-precio">
          <span>Precio de tu diseño:</span>
          <strong>{{ formulario.precio.toFixed(2) }}€</strong>
        </div>

        <button type="submit" class="btn-añadir" :disabled="cargando">
          {{ cargando ? 'Guardando...' : '🛒 Añadir encargo a la cesta' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.encargo-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); max-width: 600px; margin: auto; }
h1 { color: #283618; text-align: center; margin-bottom: 5px; }
.subtitulo { text-align: center; color: #666; margin-bottom: 30px; }

.form-personalizar { display: flex; flex-direction: column; gap: 20px; }
.campo { display: flex; flex-direction: column; gap: 8px; }
.campo label { font-weight: bold; color: #606c38; }

input, select { padding: 12px; border: 1px solid #ccd5ae; border-radius: 8px; font-size: 1rem; }

/* Grid de Tejidos */
.tejidos-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; margin-top: 10px; }
.tejido-item { border: 2px solid #eee; border-radius: 10px; padding: 10px; text-align: center; cursor: pointer; transition: 0.3s; display: flex; flex-direction: column; align-items: center; }
.tejido-item img { width: 60px; height: 60px; object-fit: cover; border-radius: 50%; margin-bottom: 5px; }
.tejido-item span { font-size: 0.8rem; font-weight: bold; }
.tejido-item input { display: none; }
.tejido-item.seleccionado { border-color: #bc6c25; background: #fefae0; }

.resumen-precio { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-top: 1px solid #eee; margin-top: 10px; font-size: 1.2rem; }
.resumen-precio strong { color: #bc6c25; font-size: 1.5rem; }

.btn-añadir { background: #606c38; color: white; border: none; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 1.1rem; cursor: pointer; transition: 0.2s; }
.btn-añadir:hover { background: #4a532a; }
.btn-añadir:disabled { background: #ccc; }
</style>