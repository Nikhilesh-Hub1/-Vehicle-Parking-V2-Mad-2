<template>
  <div class="card h-100 shadow-sm border-primary border-2">
    <div class="card-header">
      <h5 class="card-title text-primary mb-3">
        <i class="bi bi-geo-alt-fill me-2"></i> {{ lot.prime_location_name }}
      </h5>
      <p class="mb-2 text-dark">
        <i class="bi bi-geo me-2"></i>
        <strong>Address:</strong> {{ lot.address }}, Pincode: {{ lot.pin_code }}
      </p>
      <p class="mb-2 text-muted">
        <i class="bi bi-car-front-fill me-2"></i>
        <strong>Occupancy:</strong> {{ lot.available_spots }} / {{ lot.number_of_spots }}
      </p>
      <p class="mb-2 text-success">
        <i class="bi bi-currency-rupee me-2"></i>
        <strong>Price:</strong> ₹{{ lot.price_per_hour }} per hour
      </p>
      <!-- Edit and Delete buttons -->
      <div class="mt-3 d-flex justify-content-between">
        <button class="btn btn-sm btn-warning" @click="$emit('edit-lot', lot.id)">Edit</button>
        <button class="btn btn-sm btn-danger" @click="$emit('delete-lot', lot.id)">Delete</button>
      </div>
    </div>

    <div class="card-body">
      <!-- Grid display -->
      <div
        v-for="(row, rowIndex) in lot.grid"
        :key="rowIndex"
        class="d-flex justify-content-center mb-1"
      >
        <span
          v-for="(cell, cellIndex) in row"
          :key="cellIndex"
          class="badge me-2 p-3 fs-4"
          :class="{
            'bg-success': cell.status === 'A',
            'bg-danger': cell.status === 'O',
            'bg-secondary': cell.status === ' ',
            'cursor-pointer': cell.status !== ' ',
          }"
          @click="cell.status !== ' ' && openSpot(cell)"
        >
          {{ cell.status }}
        </span>
      </div>

      <!-- Modal for Available Spot -->
      <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
        <div class="modal-content">
          <h5>Spot Details</h5>
          <p><strong>Lot ID:</strong> {{ selectedSpot.lot_id }}</p>
          <p><strong>Spot ID:</strong> {{ selectedSpot.id }}</p>
          <p>
            <strong>Status:</strong> {{ selectedSpot.status === 'O' ? 'Occupied' : 'Available' }}
          </p>
          <div class="mt-3 d-flex gap-2">
            <button class="btn btn-danger" @click="deleteSpot">Delete</button>
            <button class="btn btn-secondary" @click="closeModal">Cancel</button>
          </div>
        </div>
      </div>

      <!-- Modal for Occupied Spot -->
      <div v-if="spotDetailsModal" class="modal-backdrop" @click.self="closeOccupiedModal">
        <div class="modal-content">
          <h5>Occupied Parking Spot Details</h5>
          <p><strong>Spot ID:</strong> {{ spotDetails.spot_id }}</p>
          <p><strong>Reservation ID:</strong> {{ spotDetails.id }}</p>
          <p><strong>Customer ID:</strong> {{ spotDetails.user_id }}</p>

          <p><strong>Vehicle Number:</strong> {{ spotDetails.vehicle_number }}</p>
          <p>
            <strong>Date/Time of Parking:</strong>
            {{ formatDate(spotDetails.parking_timestamp) }}
          </p>

          <div class="mt-3">
            <button class="btn btn-secondary" @click="closeOccupiedModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: { lot: Object },
  data() {
    return {
      showModal: false,
      spotDetailsModal: false,
      selectedSpot: { status: null, id: null, lot_id: null },
      spotDetails: {},
    }
  },
  methods: {
    openSpot(cell) {
      this.selectedSpot = { status: cell.status, id: cell.id, lot_id: cell.lot_id }
      if (cell.status === 'O') {
        this.viewOccupiedSpots()
      } else {
        this.showModal = true
      }
    },
    closeModal() {
      this.showModal = false
    },
    closeOccupiedModal() {
      this.spotDetailsModal = false
    },

    async viewOccupiedSpots() {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/reservations/by_spot/${this.selectedSpot.id}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } },
        )
        if (!res.ok) throw new Error(await res.text())
        this.spotDetails = await res.json()
        this.spotDetailsModal = true
      } catch (err) {
        console.error('Error fetching spot details:', err)
        alert('Could not load reservation details')
      }
    },

    deleteSpot() {
      if (this.selectedSpot.status !== 'A') {
        alert('Only available spots can be deleted.')
        return
      }
      if (!confirm('Delete this parking spot?')) return
      fetch(`http://127.0.0.1:5000/api/parking_spots/${this.selectedSpot.id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      })
        .then(async (res) => {
          if (!res.ok) throw new Error(await res.text())
          this.updateLocalSpotData()
          this.showModal = false
          alert('Spot deleted successfully!')
        })
        .catch((err) => {
          console.error('Delete failed:', err)
          alert(err.message || 'Deletion failed')
        })
    },

    updateLocalSpotData() {
      this.lot.grid.forEach((row) => {
        row.forEach((cell, index) => {
          if (cell.id === this.selectedSpot.id) row.splice(index, 1)
        })
      })
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    },
  },
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1050;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}
.cursor-pointer {
  cursor: pointer;
}
</style>
