<template>
  <div class="container mt-4">
    <h2 class="mb-4">Welcome, {{ user.name }}</h2>

    <!-- Search -->
    <div class="mb-3">
      <input
        type="text"
        v-model="searchQuery"
        class="form-control"
        placeholder="Search parking by location or pin code"
      />
    </div>

    <!-- Parking Lots -->
    <div>
      <h4>Parking Lots</h4>
      <div class="row">
        <div class="col-md-4 mb-3" v-for="lot in filteredLots" :key="lot.id">
          <div class="card h-100 border-primary">
            <div class="card-body">
              <h5 class="card-title text-primary">{{ lot.prime_location_name }}</h5>
              <p class="card-text">{{ lot.address }} ({{ lot.pin_code }})</p>
              <p class="card-text">Available Spots: {{ lot.available_spots }}</p>
              <p class="card-text text-success">₹ Price Per Hour: {{ lot.price_per_hour }}</p>

              <button
                class="btn btn-success"
                :disabled="lot.available_spots === 0"
                @click="openBookingModal(lot)"
              >
                Book
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Parking History -->
   <div class="container mt-4">
    <h3>Export My Parking Data</h3>
    <button class="btn btn-primary" @click="exportData">Export Reservations</button>
    <p class="mt-2 text-success">{{ message }}</p>
  </div>
    <div class="card mb-4">
      <div class="card-header bg-light"><strong>Recent Parking History</strong></div>
      <div class="card-body p-0">
        <table class="table table-bordered table-hover mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Location</th>
              <th>Vehicle No</th>
              <th>Start Time</th>
              <th>Status</th>
              <th>Paid</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in reservations" :key="res.id">
              <td>{{ res.id }}</td>
              <td>{{ res.lot_name }}</td>
              <td>{{ res.vehicle_number }}</td>
              <td>{{ formatDate(res.parking_timestamp) }}</td>
              <td>{{ res.status_message }}</td>
              <td>{{ formatCurrency(res.parking_cost) }}</td>
              <td>
                <button
                  v-if="!res.leaving_timestamp"
                  class="btn btn-sm btn-danger"
                  @click="openReleaseModal(res)"
                >
                  Release
                </button>
                <button v-else class="btn btn-sm btn-info" @click="openViewModal(res)">
                  View Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- View Reservation Details Modal -->
    <div class="modal" tabindex="-1" v-if="showViewModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reservation Details</h5>
            <button type="button" class="btn-close" @click="showViewModal = false"></button>
          </div>
          <div class="modal-body">
            <p><strong>Lot:</strong> {{ viewData.lot_name }}</p>

            <p><strong>Spot ID:</strong> {{ viewData.spot_id }}</p>
            <p><strong>Vehicle Number:</strong> {{ viewData.vehicle_number }}</p>
            <p><strong>Parking In:</strong> {{ formatDate(viewData.parking_timestamp) }}</p>
            <p><strong>Parking Out:</strong> {{ formatDate(viewData.leaving_timestamp) }}</p>
            <p><strong>Duration:</strong> {{ viewData.human_readable_duration }}</p>
            <p><strong>Price Per Hour:</strong> {{ viewData.price_per_hour }}</p>
            <p><strong>Total Cost:</strong> ₹{{ viewData.parking_cost }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showViewModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Book Parking Modal -->
    <div class="modal" tabindex="-1" v-if="showBookingModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Book Parking Spot</h5>
            <button type="button" class="btn-close" @click="showBookingModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label>Spot ID</label>
              <input type="text" v-model="bookingData.spot_id" class="form-control" readonly />
            </div>
            <div class="mb-3">
              <label>Lot ID</label>
              <input type="text" v-model="bookingData.lot_id" class="form-control" readonly />
            </div>
            <div class="mb-3">
              <label>Vehicle Number</label>
              <input type="text" v-model="bookingData.vehicle_number" class="form-control" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showBookingModal = false">Cancel</button>
            <button class="btn btn-primary" @click="confirmBooking">Reserve</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Release Parking Modal -->
    <div class="modal" tabindex="-1" v-if="showReleaseModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Release Parking Spot</h5>
            <button type="button" class="btn-close" @click="showReleaseModal = false"></button>
          </div>
          <div class="modal-body">
            <p><strong>Lot Name:</strong> {{ releaseData.lot_name }}</p>
            <p><strong>Spot ID:</strong> {{ releaseData.spot_id }}</p>
            <p><strong>Reservation ID:</strong> {{ releaseData.id }}</p>
            <p><strong>Vehicle Number:</strong> {{ releaseData.vehicle_number }}</p>
            <p><strong>Parking Time:</strong> {{ formatDate(releaseData.parking_timestamp) }}</p>
            <p><strong>Releasing Time:</strong> {{ formatDate(new Date()) }}</p>
            <p><strong>Total Cost:</strong> ₹{{ releaseData.parking_cost || 'Calculating...' }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showReleaseModal = false">Cancel</button>
            <button class="btn btn-danger" @click="confirmRelease">Release</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || {},
      token: localStorage.getItem('token'),
      parkingLots: [],
      reservations: [],
      searchQuery: '',
      showBookingModal: false,
      bookingData: { spot_id: '', lot_id: '', vehicle_number: '' },
      showReleaseModal: false,
      releaseData: {},
      showViewModal: false,
      viewData: {},
      message: "" ,
    }
  },
  computed: {
    filteredLots() {
      if (!this.searchQuery) return this.parkingLots
      return this.parkingLots.filter(
        (lot) =>
          lot.prime_location_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          lot.pin_code.includes(this.searchQuery),
      )
    },
  },
  created() {
    this.fetchLots()
    this.fetchReservations()
  },
  methods: {
    async fetchLots() {
      const res = await fetch('http://127.0.0.1:5000/api/parking_lots', {
        headers: { Authorization: `Bearer ${this.token}` },
      })
      const data = await res.json()
      this.parkingLots = data.lots || []
    },
    async fetchReservations() {
      const res = await fetch('http://127.0.0.1:5000/api/reservations', {
        headers: { Authorization: `Bearer ${this.token}` },
      })
      const data = await res.json()
      // Sort reservations by parking_timestamp (newest first)
      const sorted = data.reservations.sort(
        (a, b) => new Date(b.parking_timestamp) - new Date(a.parking_timestamp),
      )
      this.reservations = sorted
    },
    async openBookingModal(lot) {
      const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lot.id}`, {
        headers: { Authorization: `Bearer ${this.token}` },
      })
      const data = await res.json()
      const spot = data.lot.grid.flat().find((s) => s.status === 'A')
      if (!spot) return alert('No available spot')
      this.bookingData = { spot_id: spot.id, lot_id: lot.id, vehicle_number: '' }
      this.showBookingModal = true
    },
    async confirmBooking() {
      const res = await fetch('http://127.0.0.1:5000/api/reservations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.token}`,
        },
        body: JSON.stringify({
          spot_id: this.bookingData.spot_id,
          vehicle_number: this.bookingData.vehicle_number,
        }),
      })
      const data = await res.json()
      if (res.ok) {
        this.showBookingModal = false
        this.fetchLots()
        this.fetchReservations()
      } else {
        alert(data.message || 'Booking failed')
      }
    },
    openReleaseModal(reservation) {
      this.releaseData = reservation
      this.showReleaseModal = true
    },
    async confirmRelease() {
      const res = await fetch(`http://127.0.0.1:5000/api/reservations/end/${this.releaseData.id}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${this.token}` },
      })
      const data = await res.json()
      if (res.ok) {
        this.showReleaseModal = false
        this.fetchLots()
        this.fetchReservations()
      } else {
        alert(data.message || 'Error releasing spot')
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    },
    formatCurrency(amount) {
      if (amount === null || amount === undefined) return '—'
      return Number(amount).toLocaleString('en-IN', {
        style: 'currency',
        currency: 'INR',
      })
    },

    openViewModal(reservation) {
      this.viewData = reservation
      this.showViewModal = true
    },
    async exportData() {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/user/export-reservations', {
      method: 'POST',
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });

    // Check if response is JSON
    const contentType = res.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      const data = await res.json();
      this.message = data.message;
    } else {
      this.message = "Export triggered successfully!";
    }

  } catch (err) {
    this.message = "Failed to trigger export.";
  }
}

    
  },
}
</script>

<style scoped>
.modal {
  display: block;
  background: rgba(0, 0, 0, 0.5);
}
.modal-dialog {
  margin-top: 10%;
}
</style>
