<template>
  <div class="user-list">
    <br />
    <button class="btn btn-primary" @click="exportUsers">Export All Users (CSV)</button>
    <p>{{ message }}</p>
    <h2>Registered Users</h2>

    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      message: '',
    }
  },
  async mounted() {
    await this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/users', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) throw new Error('Failed to fetch users')

        const responseData = await response.json()

        this.users = responseData.users
      } catch (error) {
        console.error('Error:', error)
        alert('Could not load users')
      }
    },
    async exportUsers() {
      try {
        const res = await fetch('http://127.0.0.1:5000/api/admin/export-users', {
          method: 'POST',
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        })
        const data = await res.json()
        this.message = data.message
      } catch (err) {
        this.message = 'Failed to trigger user export.'
      }
    },
  },
}
</script>
