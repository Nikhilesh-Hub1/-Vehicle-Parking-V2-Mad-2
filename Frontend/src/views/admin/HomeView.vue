<template>
  <div class="container-fluid p-4">
    <!-- Topbar -->
    <header>
      <div
        class="d-flex justify-content-between align-items-center bg-light p-3 rounded mb-4 shadow-sm"
      >
        <div>
          💚 Welcome, Admin | 🧑 <a href="#">Users</a> | 🔍 <a href="#">Search</a> | 📊
          <a href="#">Summary</a> | 🚪 <a href="#">Logout</a>
        </div>
        <div class="text-end">🖼️ <strong>Admin Profile</strong></div>
      </div>
    </header>

    <h4 class="text-center text-primary mb-4">🚗 Parking Lots</h4>

    <!-- Grid of Parking Lot Cards -->
    <div class="row g-4">
      <!-- Add New Lot Card -->
      <div class="col-md-4">
        <div
          class="card h-100 align-items-center justify-content-center border border-2 border-primary text-center bg-light"
        >
          <button class="btn btn-outline-primary" @click="goToAddLot">➕ Add Lot</button>
        </div>
      </div>
      <div class="col-md-4" v-for="lot in parkingLots" :key="lot.id">
        <ParkingLot :lot="lot" @edit-lot="goToEditLot" @delete-lot="deleteLot" />
      </div>
    </div>
  </div>
</template>

<script>
import ParkingLot from './ParkingLot.vue'

export default {
  components: { ParkingLot },
  data() {
    return {
      parkingLots: [],
    }
  },
  methods: {
    goToAddLot() {
      this.$router.push('/admin/parkinglots/add')
    },
    fetchParkingLots() {
      fetch('http://127.0.0.1:5000/api/parking_lots', {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
        .then(async (res) => {
          if (res.status === 401 || res.status === 403) {
            alert('Session expired. Please login again.')
            localStorage.removeItem('token')
            this.$router.push('/in')
            return
          }

          const data = await res.json()
          this.parkingLots = data.lots
          console.log('Parking lots fetched:', this.parkingLots)
        })
        .catch((err) => {
          console.error('Error fetching parking lots:', err)
        })
    },

    async deleteLot(lotId) {
      const confirmDelete = confirm('Are you sure you want to delete this lot?')
      if (!confirmDelete) return

      try {
        const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lotId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })

        if (res.ok) {
          // Remove from local list
          if (Array.isArray(this.parkingLots)) {
            this.parkingLots = this.parkingLots.filter((lot) => lot.id !== lotId)
          }
          this.fetchParkingLots()
        } else {
          console.error('Delete failed')
        }
      } catch (err) {
        console.error('Error deleting lot:', err)
      }
    },
    goToEditLot(lotId) {
      this.$router.push(`/admin/parkinglots/edit/${lotId}`)
    },
  },
  mounted() {
    this.fetchParkingLots()
  },
}
</script>
