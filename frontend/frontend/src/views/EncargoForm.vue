<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const tejidos = ref([])
const cargando = ref(false)

const preciosBase = {
  'Mochila Personalizada': 45.0,
  'Bolsa de Muda / Merienda': 22.0,
  'Estuche Enrollable': 18.0,
  'Babero Personalizado Clásico': 18.0,
  'Babero Bandana (Pack 2)': 16.0,
  'Cambiador Personalizado': 28.0,
  'Neceser Gran Capacidad': 25.0,
  'Arrullo / Manta Ligera': 38.0,
  'Funda Cartilla Sanitaria': 26.0,
  'Chupetero de Tela y Madera': 14.0,
  'Bolsita Guarda Chupetes': 10.0,
  'Cesta Organizadora de Tela': 20.0,
  'Cojín Decorativo Bordado': 24.0,
  'Guirnalda de Banderines': 22.0
}

const formulario = ref({
  id_producto: null,
  producto_type: 'Mochila Personalizada',
  id_tejido: '',
  bordado: '',
  precio: 45.0,
  estado: 'CARRITO'
})

onMounted(async () => {
  try {
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
    await axios.post('http://127.0.0.1:8000/api/encargos/', formulario.value)
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
