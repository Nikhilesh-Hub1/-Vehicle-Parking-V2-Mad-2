<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <label for="email">Email:</label>
      <input type="email" id="email" name="email" v-model="email" required />
      <br />
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" v-model="password" required />
      <br />
      <input type="submit" value="Submit" />
    </form>

    <p>Don't have an account? <router-link to="#">Register here</router-link></p>
    <p style="color: red">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      email: 'pam@gmail.com',
      password: 'nikhilesh',
      message: '',
    }
  },
  methods: {
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
