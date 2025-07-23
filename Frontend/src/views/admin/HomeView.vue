<template>
  <div class="container-fluid p-4">
    <!-- Search -->
    <div class="mb-3">
      <input
        type="text"
        v-model="searchQuery"
        class="form-control"
        placeholder="Search parking by location or pin code"
      />
    </div>

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
      <div class="col-md-4" v-for="lot in filteredLots" :key="lot.id">
        <ParkingLot
          :lot="lot"
          @edit-lot="goToEditLot"
          @delete-lot="deleteLot"
          @spot-updated="fetchParkingLots"
        />
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
      searchQuery: '',
    }
  },
  computed: {
    filteredLots() {
      const query = this.searchQuery.trim().toLowerCase()
      if (!query) return this.parkingLots
      return this.parkingLots.filter(
        (lot) =>
          lot.prime_location_name.toLowerCase().includes(query) ||
          lot.pin_code.toString().toLowerCase().includes(query),
      )
    },
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
      const lot = this.parkingLots.find((l) => l.id === lotId)
      if (!lot) return

      // Flatten the grid to get a simple array of spots
      const allSpots = lot.grid.flat()

      // Check if any spot is NOT available
      const hasOccupied = allSpots.some((spot) => spot.status !== 'A')

      if (hasOccupied) {
        alert('Cannot delete this lot. Some spots are still occupied.')
        return
      }

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
