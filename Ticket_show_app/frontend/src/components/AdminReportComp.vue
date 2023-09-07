<template>
  <div class="reports-container">
    <b-button @click="download" sticky class="sticky-btn">Download</b-button>
    <h2>All Reports</h2>
    <div v-for="(report, index) in reports" :key="index" class="report">
      <h3 class="report-title">{{ report.title }}</h3>
      <div v-if="report.dataType === 'list'" class="report-list">
        <ul>
          <li v-for="(item, key) in report.data" :key="key">{{ item }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      reports: [],
    };
  },
  async created() {
    const reportEndpoints = [
      'tickets_booked_per_show',
      'total_revenue_per_show',
      'top_rated_shows',
      'total_tickets_sold',
      'shows_by_venue',
      'users_with_most_bookings',
      'venue_with_highest_sales',
    ];

    try {
      const responsePromises = reportEndpoints.map(endpoint => {
        return axios.get(`http://127.0.0.1:5000/admin/reports/${endpoint}`, {
          headers: { 'x-access-token': localStorage.getItem('token') },
        });
      });

      const responses = await axios.all(responsePromises);

      this.reports = responses.map((response, index) => {
        return {
          title: reportEndpoints[index].replace(/_/g, ' ').toUpperCase(),
          data: response.data,
          dataType: 'list', // Assuming the initial data type is a list, update this accordingly
        };
      });
    } catch (error) {
      console.error(error);
    }
  },
  methods :
  {
    download() {
      window.print()
    },
  }
};
</script>

<style>
.reports-container {
  margin: 20px;
  position: relative;
  background-color:white;
}

.report {
  margin-bottom: 30px;
  border: 1px solid #ccc;
/* Chrome 10-25, Safari 5.1-6 */
background: -webkit-linear-gradient(to right, rgba(106, 17, 203, 1), rgba(37, 117, 252, 1));

/* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
background: linear-gradient(to right, rgba(106, 17, 203, 1), rgba(37, 117, 252, 1));
  padding: 15px;
}

.report-title {
  margin: 0;
  padding-bottom: 10px;
  color:white;
  border-bottom: 1px solid #ccc;
}

.report-list {
  margin-top: 10px;
  color:white;
}

.report-table {
  margin-top: 10px;
  color:white;
}

table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ccc;
}


th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.sticky-btn {
  position: fixed;
  bottom: 20px; /* Adjust as needed */
  right: 40px; /* Adjust as needed */
  padding: 10px 20px;
  background-color:dimgray;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
