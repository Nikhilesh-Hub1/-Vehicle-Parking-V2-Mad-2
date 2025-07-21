<template>
  <div class="container mt-4">
    <h4 class="mb-3">Add New Parking Lot</h4>

    <form @submit.prevent="submitLot">
      <div class="mb-3">
        <label class="form-label">Prime Location Name</label>
        <input type="text" v-model="lot.prime_location_name" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Price per Hour</label>
        <input type="number" v-model="lot.price" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Address</label>
        <textarea v-model="lot.address" class="form-control" required></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label">Pin Code</label>
        <input type="text" v-model="lot.pin_code" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Number of Spots</label>
        <input type="number" v-model="lot.number_of_spots" class="form-control" required />
      </div>

      <button type="submit" class="btn btn-primary">Create Lot</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lot: {
        prime_location_name: '',
        price: '',
        address: '',
        pin_code: '',
        number_of_spots: '',
      },
    }
  },
  methods: {
    async submitLot() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/parking_lots', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token'),
          },
          body: JSON.stringify(this.lot),
        })

        if (!response.ok) throw new Error('Failed to create parking lot')

        alert('Parking lot created successfully!')
        this.$router.push('/admin')
      } catch (error) {
        console.error(error)
        alert('Error creating parking lot')
      }
    },
  },
}
</script>
