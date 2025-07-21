<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <header>
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="50" height="50" />
      <h1>Vehicle Parking System</h1>

      <div class="wrapper">
        <nav v-if="isAdmin">
          <RouterLink v-if="isAdmin" to="/admin">Admin Dashboard</RouterLink>
          <RouterLink to="/about">About</RouterLink>
          <RouterLink v-if="!isLoggedIn" to="/in">Login/Register</RouterLink>
          <a v-if="isLoggedIn" @click="logout">Logout</a>
        </nav>

        <nav v-else>
          <RouterLink v-if="isLoggedIn" to="/user/dashboard">Dashboard</RouterLink>
          <RouterLink to="/about">About</RouterLink>
          <RouterLink v-if="!isLoggedIn" to="/in">Login/Register</RouterLink>
          <a v-if="isLoggedIn" @click="logout">Logout</a>
        </nav>
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
      isAdmin: false,
    }
  },
  created() {
    const token = localStorage.getItem('token')
    const user = JSON.parse(localStorage.getItem('user'))
    this.isLoggedIn = !!token
    this.isAdmin = user && user.role === 'admin'
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
  background-color: #42b983;
  color: white;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
