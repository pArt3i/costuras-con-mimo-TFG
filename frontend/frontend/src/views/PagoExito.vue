<template>
  <div class="exito-container">
    <div class="check-icon">✔</div>
    <h1>¡Pago Realizado con Éxito!</h1>
    <p>Hemos recibido tu pedido correctamente. En breve nos pondremos manos a la obra.</p>
    <router-link to="/" class="btn-home">Volver a la tienda</router-link>
  </div>
</template>

<style scoped>
.exito-container { text-align: center; padding: 100px 20px; }
.check-icon { 
  font-size: 50px; color: white; background: #606c38; 
  width: 100px; height: 100px; line-height: 100px; 
  border-radius: 50%; margin: 0 auto 20px;
}
.btn-home {
  display: inline-block; margin-top: 20px; padding: 10px 20px;
  background: #bc6c25; color: white; text-decoration: none; border-radius: 5px;
}
</style>