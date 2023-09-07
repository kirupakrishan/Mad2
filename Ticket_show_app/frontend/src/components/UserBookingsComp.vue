<template>
  <div>
    <div v-if="loading">
      <b-spinner></b-spinner>
    </div>
    <div v-else>
      <div style="margin-top: 10px">
        <div class="scroll-container">
            <div
              v-for="ticket in tickets"
              :key="ticket.id"
              class="scroll-item"
            >
            <b-card
    :title="ticket.name"
    :img-src="`http://127.0.0.1:5000/home/show/get/img/${ticket.show_id}`"
    img-height="200px"
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 300px"
    class="mb-2"
    >
    <b-container>
      <b-row>
        <b-col style="padding: 5px">Time:{{ ticket.time }}</b-col>
        <b-col style="padding: 5px">Date:{{ ticket.date }}</b-col>
      </b-row>
      <b-row>
        <b-row>
          <b-col
            >Total Seats : {{ ticket.seats }}</b-col
          >
          <b-col
            >Total Price : {{ ticket.price }}</b-col
          >
        </b-row>
        <b-col>Tags : {{ ticket.tags }}</b-col>
      </b-row>
      <b-row>
        <b-col>
          <div>
            <b-form-rating
              readonly
              v-model="ticket.rating"
              show-value
              show-value-max
              precision="1"
            ></b-form-rating>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </b-card>
              
</div>
        </div>
      </div>
    </div>
  </div>
</template>
  <script>
import axios from "axios";
export default {
  data() {
    return {
      tickets: {},
      user_id: 1,
      loading: true,
    };
  },
  mounted() {
    this.getBookedShows();
  },
  methods: {
    async getBookedShows() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/booking/show/getall`
          ,{headers: { 'x-access-token': localStorage.getItem('token') }}
        );
        this.tickets = res.data.booked;
        console.log(this.tickets);
      } catch (err) {
        console.log(err);
      }
      this.loading = false;
    },
  },
};
</script>
  <style>
.scroll-container {
  width: 100%; /* Set the desired width of the container */
  display: flex; /* Ensure the list items are in a row */
  flex-wrap: wrap;
  gap:10px;
  padding: 0;
  margin: 0;
  list-style: none;
  white-space: nowrap; /* Prevent wrapping of items to a new line */
}

.scroll-item {
  /* Add your desired styles for the items */
  flex: 0 0 calc(25% - 20px);
  padding: 10px;
  margin: 5px;
  text-align: center;
}
</style>