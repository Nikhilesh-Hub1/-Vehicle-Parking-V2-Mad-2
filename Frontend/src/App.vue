<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <div class="wrapper">
      <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #e3f2fd">
        <div class="container-fluid">
          <!-- Logo -->
          <RouterLink class="navbar-brand" to="/about">
            <img
              alt="logo"
              src="@/assets/logo.svg"
              width="30"
              height="30"
              class="d-inline-block align-top"
            />
            <b style="color: green">Vehicle Parking</b>
          </RouterLink>

          <!-- Links -->
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
              <!-- Admin Links -->
              <template v-if="isAdmin && isLoggedIn">
                <li class="nav-item">
                  <RouterLink class="nav-link" to="/admin">Admin Dashboard</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link" to="/admin/userslist">Users</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link" to="/admin/summary">Summary</RouterLink>
                </li>
              </template>

              <!-- User Links -->
              <template v-else-if="isLoggedIn">
                <li class="nav-item">
                  <RouterLink class="nav-link" to="/user/dashboard">Dashboard</RouterLink>
                </li>
              </template>

              <!-- Common Links -->
              <li class="nav-item">
                <RouterLink class="nav-link" to="/about">About</RouterLink>
              </li>

              <li class="nav-item" v-if="!isLoggedIn">
                <RouterLink class="nav-link" to="/in">Login/Register</RouterLink>
              </li>

              <li class="nav-item" v-if="isLoggedIn">
                <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>

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
