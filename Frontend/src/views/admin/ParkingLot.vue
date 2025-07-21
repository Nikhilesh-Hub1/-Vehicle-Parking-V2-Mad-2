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
            'bg-success': cell === 'A',
            'bg-danger': cell === 'O',
            'bg-secondary': cell === ' ',
          }"
        >
          {{ cell }}
        </span>
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
  methods: {},
}
</script>
