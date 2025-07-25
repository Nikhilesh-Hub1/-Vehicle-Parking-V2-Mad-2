<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow-lg border-0 rounded-4">
          <div class="card-body">
            <h2 class="text-center mb-4">{{ islogin ? 'Login' : 'Register' }}</h2>

            <form @submit.prevent="islogin ? loginUser() : registerUser()">
              <div v-if="!islogin" class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" id="name" class="form-control" v-model="name" required />
              </div>

              <div class="mb-3">
                <label :for="islogin ? 'email' : 'reg-email'" class="form-label">Email</label>
                <input
                  type="email"
                  :id="islogin ? 'email' : 'reg-email'"
                  class="form-control"
                  v-model="email"
                  required
                />
              </div>

              <div class="mb-3">
                <label :for="islogin ? 'password' : 'reg-password'" class="form-label"
                  >Password</label
                >
                <input
                  type="password"
                  :id="islogin ? 'password' : 'reg-password'"
                  class="form-control"
                  v-model="password"
                  required
                />
              </div>

              <button type="submit" class="btn btn-primary w-100 mb-3">
                {{ islogin ? 'Login' : 'Register' }}
              </button>
            </form>

            <p class="text-center">
              {{ islogin ? "Don't have an account?" : 'Already have an account?' }}
              <button type="button" class="btn btn-link p-0" @click="toggleLogin">
                {{ islogin ? 'Register here' : 'Login' }}
              </button>
            </p>

            <p class="text-danger text-center">{{ message }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthView',
  data() {
    return {
      islogin: true,
      name: '',
      email: '',
      password: '',
      message: '',
    }
  },
  methods: {
    toggleLogin() {
      this.islogin = !this.islogin
      this.message = ''
    },
    async loginUser() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.email, password: this.password }),
        })

        if (response.ok) {
          const data = await response.json()
          this.message = data.message || 'Login successful'
          localStorage.setItem('token', data.access_token)
          localStorage.setItem('user', JSON.stringify(data.user))

          if (data.user.role === 'admin') {
            this.$router.push({ name: 'admin' })
          } else {
            this.$router.push({ name: 'user-dashboard' })
          }
          window.location.reload()
        } else {
          const errorData = await response.json()
          this.message = errorData.message || 'Login failed'
        }
      } catch (error) {
        this.message = 'Network error. Please try again.'
      }
    },
    async registerUser() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            password: this.password,
          }),
        })

        if (response.ok) {
          const data = await response.json()
          this.message = data.message || 'Registration successful'
          alert('Registration successful! Please log in to continue.')
          this.islogin = true
          this.email = ''
          this.password = ''
        } else {
          const errorData = await response.json()
          this.message = errorData.message || 'Registration failed'
        }
      } catch (error) {
        this.message = 'Network error. Please try again.'
      }
    },
  },
}
</script>
