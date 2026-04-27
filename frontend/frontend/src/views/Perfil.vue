<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const usuarioActual = ref({ email: '', username: '' })
const nuevoEmail = ref('')
const nuevaPass = ref('')
const mensaje = ref({ texto: '', tipo: '' })

// Cargar datos al iniciar
onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:8000/api/usuarios/me/', {
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  })
  usuarioActual.value = res.data
  nuevoEmail.value = res.data.email
})

const apiUpdate = async (datos) => {
  try {
    await axios.patch('http://127.0.0.1:8000/api/usuarios/me/', datos, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    mensaje.value = { texto: "✅ Cambio realizado con éxito", tipo: 'exito' }
    // Actualizamos la vista del email actual si cambió
    if(datos.email) usuarioActual.value.email = datos.email
  } catch (error) {
    const errorMsg = error.response?.data?.email?.[0] || error.response?.data?.password?.[0] || "Error al actualizar";
    mensaje.value = { texto: `❌ ${errorMsg}`, tipo: 'error' }
  }
}

const cambiarCorreo = () => {
  if (nuevoEmail.value === usuarioActual.value.email) {
    mensaje.value = { texto: "Introduce un correo diferente al actual", tipo: 'error' }
    return
  }
  apiUpdate({ email: nuevoEmail.value })
}

const cambiarPass = () => {
  if (nuevaPass.value.length < 8) {
    mensaje.value = { texto: "La contraseña debe tener al menos 8 caracteres", tipo: 'error' }
    return
  }
  apiUpdate({ password: nuevaPass.value })
}
</script>

<template>
    <div class="container perfil-container">
        <div class="form-card">
            <h1>👤 Gestión de Perfil</h1>
            <p>Usuario: <strong>{{ usuarioActual.username }}</strong></p>

            <div v-if="mensaje.texto" :class="['alerta', mensaje.tipo]">{{ mensaje.texto }}</div>

            <section class="seccion-perfil">
                <h3>Cambiar Correo Electrónico</h3>
                <input type="email" v-model="nuevoEmail" class="input-estilo">
                <button @click="cambiarCorreo" class="btn-primario">Actualizar Email</button>
            </section>

        <hr>

        <section class="seccion-perfil">
            <h3>Cambiar Contraseña</h3>
            <input type="password" v-model="nuevaPass" placeholder="Mínimo 8 caracteres" class="input-estilo">
            <button @click="cambiarPass" class="btn-primario">Actualizar Contraseña</button>
        </section>
    </div>
</div>
</template>

<style scoped>
.perfil-container { max-width: 500px; margin-top: 40px; }
.seccion-perfil { margin: 20px 0; display: flex; flex-direction: column; gap: 10px; }
.input-estilo { padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
</style>