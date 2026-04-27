<template>
  <div v-if="mostrar" class="modal-overlay" @click.self="$emit('cerrar')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('cerrar')">×</button>
      <h2>Acceder a tu cuenta</h2>
      
      <form @submit.prevent="hacerLogin">
        <div class="input-group">
          <label>Usuario</label>
          <input v-model="form.username" type="text" required placeholder="Tu nombre de usuario">
        </div>
        <div class="input-group">
          <label>Contraseña</label>
          <input v-model="form.password" type="password" required placeholder="••••••••">
        </div>
        
        <button type="submit" class="btn-login" :disabled="cargando">
          {{ cargando ? 'Verificando...' : 'Entrar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const props = defineProps(['mostrar'])
const emit = defineEmits(['cerrar', 'loginExitoso'])
const router = useRouter()

const form = ref({ username: '', password: '' })
const cargando = ref(false)

const hacerLogin = async () => {
  cargando.value = true
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/token/', form.value)
    
    localStorage.setItem('token', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    localStorage.setItem('username', form.value.username)

    const resUser = await axios.get('http://127.0.0.1:8000/api/usuarios/me/', {
      headers: { Authorization: `Bearer ${res.data.access}` }
    })

    const esAdmin = resUser.data.is_superuser
    localStorage.setItem('isAdmin', esAdmin)

    emit('loginExitoso')
    emit('cerrar')

    if (esAdmin) {
      router.push('/admin')
    } else {
      router.push('/')
    }

  } catch (error) {
    console.error(error)
    alert("Usuario o contraseña incorrectos")
  } finally {
    cargando.value = false
  }
}
</script>