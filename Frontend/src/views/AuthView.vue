<template>
  <div v-if="islogin">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <label for="email">Email:</label>
      <input type="email" id="email" name="email" v-model="email" required />
      <br />
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" v-model="password" required />
      <br />
      <input type="submit" value="Login" />
    </form>
    <p>Don't have an account? <button type="button" @click="toggleLogin">Register here</button></p>
    <p style="color: red">{{ message }}</p>
  </div>
  <div v-else>
    <form @submit.prevent="registerUser">
      <h2>Register</h2>
      <label for="name">Name:</label>
      <input type="text" id="name" name="name" v-model="name" required />
      <br />
      <label for="reg-email">Email:</label>
      <input type="email" id="reg-email" name="email" v-model="email" required />
      <br />
      <label for="reg-password">Password:</label>
      <input type="password" id="reg-password" name="password" v-model="password" required />
      <br />
      <input type="submit" value="Register" />
    </form>
    <p>Already have an account? <button type="button" @click="toggleLogin">Login</button></p>
    <p style="color: red">{{ message }}</p>
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
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        })

        if (response.ok) {
          const data = await response.json()
          this.message = data.message || 'Login successful'
          console.log('Login successful:', data)
          localStorage.setItem('token', data.access_token)
          localStorage.setItem('user', JSON.stringify(data.user))
          window.location.reload()
          this.$router.push({ name: 'home' })
        } else {
          const errorData = await response.json()
          this.message = errorData.message || 'Login failed'
          console.error('Login failed:', response)
        }
      } catch (error) {
        this.message = 'Network error. Please try again.'
        console.error('Fetch error:', error)
      }
    },
    async registerUser() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            password: this.password,
          }),
        })

        if (response.ok) {
          const data = await response.json()
          this.message = data.message || 'Registration successful'
          console.log('Registration successful:', data)

          this.islogin = true
          this.email = ''
          this.password = ''
        } else {
          const errorData = await response.json()
          this.message = errorData.message || 'Registration failed'
          console.error('Registration failed:', response)
        }
      } catch (error) {
        this.message = 'Network error. Please try again.'
        console.error('Fetch error:', error)
      }
    },
  },
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  align-items: center;
}
label,
input {
  margin: 5px 0;
}
h2,
p {
  margin-bottom: 20px;
  text-align: center;
}
</style>
