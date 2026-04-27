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
    // 1. Pedimos el Token JWT a Django
    const res = await axios.post('http://127.0.0.1:8000/api/token/', form.value)
    
    // 2. Guardamos la sesión en el navegador
    localStorage.setItem('token', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    localStorage.setItem('username', form.value.username)

    // 3. Pedimos los datos del usuario para saber su rol
    const resUser = await axios.get('http://127.0.0.1:8000/api/usuarios/me/', {
      headers: { Authorization: `Bearer ${res.data.access}` }
    })

    const esAdmin = resUser.data.is_superuser
    localStorage.setItem('isAdmin', esAdmin)

    // Avisamos a App.vue de que todo ha ido bien y cerramos el modal
    emit('loginExitoso')
    emit('cerrar')

    // 4. Redirección Inteligente
    if (esAdmin) {
      router.push('/admin') // Si es administrador, directo al backoffice
    } else {
      router.push('/') // Si es un cliente normal, se queda en la tienda
    }

  } catch (error) {
    console.error(error)
    alert("Usuario o contraseña incorrectos")
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
.modal-overlay { 
  position: fixed; 
  top: 0; left: 0; width: 100%; height: 100%; 
  background: rgba(0,0,0,0.6); 
  display: flex; justify-content: center; align-items: center; 
  z-index: 100000; 
  backdrop-filter: blur(3px);
}

.modal-content { 
  background: #fdfaf0; 
  padding: 40px; 
  border-radius: 15px; 
  width: 350px; 
  position: relative;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.modal-content h2 {
  color: #283618;
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 1.4rem;
  text-align: center;
}

.close-btn { 
  position: absolute; 
  top: 15px; right: 20px; 
  border: none; background: none; 
  font-size: 1.5rem; cursor: pointer; 
  color: #606c38;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #bc6c25;
}

.input-group { 
  margin-bottom: 20px; 
  display: flex; flex-direction: column; gap: 8px; 
}

.input-group label {
  font-weight: bold;
  color: #606c38;
  font-size: 0.9rem;
}

.input-group input { 
  padding: 12px; 
  border: 1px solid #ccd5ae; 
  border-radius: 8px; 
  font-size: 1rem;
  outline: none;
  background: white;
}

.input-group input:focus {
  border-color: #606c38;
  box-shadow: 0 0 5px rgba(96, 108, 56, 0.2);
}

.btn-login { 
  width: 100%; 
  padding: 14px; 
  background: #606c38; 
  color: white; 
  border: none; 
  border-radius: 8px; 
  font-weight: bold; 
  cursor: pointer; 
  font-size: 1.1rem;
  margin-top: 10px;
  transition: background 0.3s;
}

.btn-login:hover:not(:disabled) {
  background: #4a532a;
}

.btn-login:disabled {
  background: #ccd5ae;
  cursor: not-allowed;
}
</style>