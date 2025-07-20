<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <header>
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="50" height="50" />

      <div class="wrapper">
        <nav>
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/about">About</RouterLink>
          <RouterLink to="/in">Auth</RouterLink>
          <a v-if="isLoggedIn" @click="logout">Logout</a>
        </nav>
        <h1>Vehicle Parking System</h1>
      </div>
    </header>

    <RouterView />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false,
    }
  },
  created() {
    this.isLoggedIn = !!localStorage.getItem('token')
  },
  methods: {
    logout() {
      if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        this.$router.push({ name: 'auth' })
        this.isLoggedIn = false
      }
    },
  },
}
</script>

<style scoped>
header {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
