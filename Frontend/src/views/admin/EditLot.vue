<template>
  <div class="container mt-5">
    <h3 class="text-center text-primary mb-4">✏️ Edit Parking Lot</h3>

    <form @submit.prevent="updateLot" class="border p-4 rounded shadow-sm bg-light">
      <div class="mb-3">
        <label class="form-label">Prime Location Name</label>
        <input v-model="lot.prime_location_name" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Price per Hour</label>
        <input
          v-model.number="lot.price_per_hour"
          type="number"
          class="form-control"
          required
          min="0"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Address</label>
        <input v-model="lot.address" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Pin Code</label>
        <input v-model="lot.pin_code" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Number of Spots</label>
        <input
          v-model.number="lot.number_of_spots"
          type="number"
          class="form-control"
          required
          min="1"
        />
      </div>

      <div class="d-flex justify-content-between">
        <button type="submit" class="btn btn-primary">Update</button>
        <button class="btn btn-secondary" @click.prevent="$router.push('/admin')">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lot: {
        prime_location_name: '',
        price_per_hour: 0,
        address: '',
        pin_code: '',
        number_of_spots: 0,
      },
    }
  },
  methods: {
    async fetchLotDetails() {
      const lotId = this.$route.params.id
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lotId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        const data = await res.json()
        this.lot = data.lot
      } catch (err) {
        console.error('Error fetching lot:', err)
      }
    },
    async updateLot() {
      const lotId = this.$route.params.id
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/parking_lots/${lotId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify(this.lot),
        })

        if (res.ok) {
          alert('Parking lot updated successfully!')
          this.$router.push('/admin')
        } else {
          alert('Failed to update parking lot.')
        }
      } catch (err) {
        console.error('Error updating lot:', err)
      }
    },
  },
  mounted() {
    this.fetchLotDetails()
  },
}
</script>

<style scoped>
form {
  max-width: 600px;
  margin: 0 auto;
}
</style>
