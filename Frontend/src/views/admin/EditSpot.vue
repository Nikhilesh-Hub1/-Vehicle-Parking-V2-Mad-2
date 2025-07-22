<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal">
      <h3>Edit Spot</h3>
      <p><strong>ID:</strong> {{ spot.id }}</p>
      <p><strong>Status:</strong></p>
      <select v-model="spot.status">
        <option value="available">Available</option>
        <option value="occupied">Occupied</option>
      </select>
      <br /><br />
      <button @click="updateSpot">Save</button>
      <button @click="close">Cancel</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['visible', 'spot'])
const emit = defineEmits(['close', 'update'])

const close = () => emit('close')
const updateSpot = () => emit('update', props.spot)
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  background: white;
  padding: 1rem;
  border-radius: 10px;
  width: 300px;
}
</style>
