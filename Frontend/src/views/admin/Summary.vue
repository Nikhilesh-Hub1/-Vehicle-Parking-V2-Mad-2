<template>
  <div class="container mt-4">
    <h3 class="text-center text-primary mb-4">Admin Summary Dashboard</h3>

    <!-- Lot-wise Occupancy -->

    <div class="card mb-4">
      <div class="card-header bg-light">
        <h5 class="mb-0">Parking Lot Occupancy</h5>
      </div>

      <canvas id="lotChart"></canvas>
    </div>

    <!-- Overall Utilization -->

    <div class="card">
      <div class="card-header bg-light">
        <h5 class="mb-0">Overall Utilization</h5>
      </div>
      <div class="card-body d-flex justify-content-center">
        <div style="width: 600px; height: 700px">
          <canvas id="totalChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto'

export default {
  data() {
    return {
      chartData: null,
      totalData: null,
    }
  },
  mounted() {
    fetch('http://127.0.0.1:5000/api/admin/summary', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
    })
      .then((res) => res.json())
      .then((data) => {
        this.chartData = data.lot_summary
        this.totalData = data.totals
        this.renderCharts()
      })
      .catch((err) => console.error(err))
  },
  methods: {
    renderCharts() {
      // Lot-wise Bar Chart
      new Chart(document.getElementById('lotChart'), {
        type: 'bar',
        data: {
          labels: this.chartData.map((l) => l.lot_name),
          datasets: [
            {
              label: 'Available',
              data: this.chartData.map((l) => l.available),
              backgroundColor: '#28a745',
            },
            {
              label: 'Occupied',
              data: this.chartData.map((l) => l.occupied),
              backgroundColor: '#dc3545',
            },
          ],
        },
      })

      // Overall Pie Chart
      new Chart(document.getElementById('totalChart'), {
        type: 'pie',
        data: {
          labels: ['Available', 'Occupied'],
          datasets: [
            {
              data: [this.totalData.available, this.totalData.occupied],
              backgroundColor: ['#28a745', '#dc3545'],
            },
          ],
        },
      })
    },
  },
}
</script>
