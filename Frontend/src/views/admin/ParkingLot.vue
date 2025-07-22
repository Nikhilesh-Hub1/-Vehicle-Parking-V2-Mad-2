<template>
  <div class="card h-100 shadow-sm border-primary border-2">
    <div class="card-header">
      <!-- Location Title -->
      <h5 class="card-title text-primary mb-3">
        <i class="bi bi-geo-alt-fill me-2"></i> {{ lot.prime_location_name }}
      </h5>

      <!-- Address -->
      <p class="mb-2 text-dark">
        <i class="bi bi-geo me-2"></i>
        <strong>Address:</strong> {{ lot.address }}, Pincode: {{ lot.pin_code }}
      </p>

      <!-- Occupancy -->
      <p class="mb-2 text-muted">
        <i class="bi bi-car-front-fill me-2"></i>
        <strong>Occupancy:</strong> {{ lot.available_spots }} / {{ lot.number_of_spots }}
      </p>

      <!-- Price -->
      <p class="mb-2 text-success">
        <i class="bi bi-currency-rupee me-2"></i>
        <strong>Price:</strong> ₹{{ lot.price_per_hour }} per hour
      </p>
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
          @click="cell.status !== ' ' && openSpotEditor(cell)"
        >
          {{ cell.status }}
        </span>
      </div>

      <!-- Spot Edit Modal -->
      <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
        <div class="modal-content">
          <h5>Edit Spot</h5>

          <p><strong>Lot ID:</strong> {{ selectedSpot.lot_id }}</p>
          <p><strong>Spot ID:</strong> {{ selectedSpot.id }}</p>

          <p><strong>Status:</strong></p>

          <select v-model="selectedSpot.status" class="form-select">
            <option value="A">Available</option>
            <option value="O">Occupied</option>
          </select>
          <div class="mt-3 d-flex gap-2">
            <button class="btn btn-primary" @click="saveSpotStatus">Save</button>
            <button class="btn btn-danger" @click="deleteSpot">Delete</button>
            <button class="btn btn-secondary" @click="closeModal">Cancel</button>
          </div>
        </div>
      </div>

      <!-- Edit and Delete buttons -->
      <div class="mt-3 d-flex justify-content-between">
        <button class="btn btn-sm btn-warning" @click="$emit('edit-lot', lot.id)">Edit</button>

        <button class="btn btn-sm btn-danger" @click="$emit('delete-lot', lot.id)">Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    lot: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      selectedSpot: {
        status: null,
        id: null,
        lot_id: null,
      },
    }
  },
  methods: {
    openSpotEditor(cell) {
      this.selectedSpot = {
        status: cell.status,
        id: cell.id, // spot_id
        lot_id: cell.lot_id,
      }

      this.showModal = true
    },
    closeModal() {
      this.showModal = false
    },
    saveSpotStatus() {
      fetch(`http://127.0.0.1:5000/api/parking_spots/${this.selectedSpot.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          lot_id: this.selectedSpot.lot_id,
          status: this.selectedSpot.status,
        }),
      })
        .then((res) => res.json())
        .then(() => {
          this.showModal = false
          this.$emit('spot-updated')
        })
        .catch((err) => {
          console.error('Error saving spot', err)
        })
    },

    deleteSpot() {
      if (!confirm('Permanently delete this parking spot?')) return

      fetch(`http://127.0.0.1:5000/api/parking_spots/${this.selectedSpot.id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
        .then(async (res) => {
          if (!res.ok) throw new Error(await res.text())

          // Directly update the local grid data
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
      // Find and remove the spot from the grid
      this.lot.grid.forEach((row) => {
        row.forEach((cell, index) => {
          if (cell.id === this.selectedSpot.id) {
            row.splice(index, 1) // Remove the spot

            // Update counts
            this.lot.number_of_spots
            if (cell.status === 'A') this.lot.available_spots
          }
        })
      })
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
