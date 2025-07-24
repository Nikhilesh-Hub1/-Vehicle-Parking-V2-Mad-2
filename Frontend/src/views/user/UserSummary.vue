<template>
  <div class="container mt-4">
    <h3 class="text-primary mb-4 text-center">Your Parking Summary</h3>

    <!-- Stats -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card shadow-sm p-3 text-center">
          <h5>Total Reservations</h5>
          <h3>{{ summary.total }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm p-3 text-center">
          <h5>Total Spent</h5>
          <h3 class="text-success">{{ formatCurrency(summary.total_spent) }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm p-3 text-center">
          <h5>Active Reservation</h5>
          <h3>{{ summary.active > 0 ? 'Yes' : 'No' }}</h3>
        </div>
      </div>
    </div>

    <!-- Chart -->
    <div class="card shadow-sm p-3">
      <h5>Summary on Already Used Parking Spots</h5>
      <div style="height: 300px;">
        <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'UserSummary',
  components: { Bar },
  data() {
    return {
      summary: {
        active: 0,
        completed: 0,
        total: 0,
        total_spent: 0,
      },
      chartData: null,
      chartOptions: {},
    }
  },
  methods: {
    async fetchData() {
      try {
        const res = await fetch('http://127.0.0.1:5000/api/user/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        if (!res.ok) throw new Error(await res.text())

        this.summary = await res.json()
        this.prepareChart()
      } catch (err) {
        console.error('Error fetching summary:', err)
        alert('Failed to load summary')
      }
    },
    prepareChart() {
      this.chartData = {
        labels: ['Active', 'Completed', 'Total'],
        datasets: [
          {
            data: [this.summary.active, this.summary.completed, this.summary.total],
            backgroundColor: ['#4ade80', '#60a5fa', '#fca5a5'], // green, blue, pink
            borderRadius: 8,
            maxBarThickness: 80,
          },
        ],
      }
      this.chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } },
      }
    },
    formatCurrency(amount) {
      return Number(amount || 0).toLocaleString('en-IN', {
        style: 'currency',
        currency: 'INR',
      })
    },
  },
  mounted() {
    this.fetchData()
  },
}
</script>

<style scoped>
.card {
  border-radius: 10px;
}
</style>
