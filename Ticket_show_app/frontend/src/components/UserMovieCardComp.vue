<template>
  <b-card
    :title="show.name"
    :img-src="`http://127.0.0.1:5000/home/show/get/img/${show.id}`"
    img-height="200px"
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 300px"
    class="mb-2"
    >
    <b-container>
      <b-row v-if="showAvailable"
        ><b-button @click="openModal" variant="primary">BOOK</b-button></b-row
      >
      <b-row>
        <b-col style="padding: 5px">Time:{{ show.time }}</b-col>
        <b-col style="padding: 5px">Date:{{ show.date }}</b-col>
      </b-row>
      <b-row>
        <b-row>
          <b-col v-if="showAvailable"
            >{{ ticket.tickets_available }}/{{
              ticket.tickets_available + ticket.tickets_booked
            }}
            Tickets Available</b-col
          >
          <b-col v-else>HOUSEFULL</b-col>
        </b-row>
        <b-col>Tags : {{ show.tags }}</b-col>
      </b-row>
      <b-row>
        <b-col>
          <div>
            <b-form-rating
              v-model="rating"
              readonly
              show-value
              show-value-max
              precision="1"
            ></b-form-rating>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <template>
      <div>
        <b-modal
          :id="modal_id"
          ref="modal"
          title="BOOK SHOW"
          @show="resetBookModal"
          @hidden="resetBookModal"
        >
        <template #modal-footer>
          <b-button size="sm" variant="primary" @click="closeModal">
                    Close
                  </b-button>        
          <b-button size="sm" variant="primary" id="ticket.show_id" @click="bookShow">
                    Book
                  </b-button>
                </template>
          <form ref="form" @submit.stop.prevent="handleSubmit">
            <b-form-group
              id="tseat-input"
              label="Enter total Seats"
              label-for="tseats"
              :state="validationState"
              style="margin-bottom: 15px;"
            >
              <b-form-input
                id="tseats"
                v-model="ticket.seats"
                @input="validateSeats"
                :state="validationState"
                trim
                required
                class="md-10"
              ></b-form-input>
              <b-form-invalid-feedback :state="validationState">
      {{ invalid_msg }}
    </b-form-invalid-feedback>
            </b-form-group>
            <b-row>
              <b-col><p>Price Per Ticket:{{ ticket_price}}</p></b-col>
              <b-col><p>Total Price:{{ ticketPrice() }}</p></b-col>
            </b-row>
          </form>
        </b-modal>
      </div>
    </template>
  </b-card>
</template>


<script>
import axios from "axios";
export default {
  props: ['show']
,
  data() {
    return {
      ticket: {
        name: "",
        seats: null,
        price: null,
        show_id:this.show.id,
        tickets_available:null,
        tickets_booked:null
      },
      user_id:1,
      rating:null,
      modal_id:null,
      ticket_price:100,
      invalid_msg :"",
      ticketsAvailableState:false,
    };
  },
  beforeMount(){
    this.rating = this.show.rating
    this.ticket.show_id = this.show.id
    this.ticket.tickets_available=this.show.tickets_available,
    this.ticket.tickets_booked=this.show.tickets_booked
    this.modal_id = 'book-show-'+String(this.ticket.show_id)
  },
  computed :{
    validationState() {
      return this.invalid_msg ? false : null;
    },
    showAvailable(){
      return this.ticket.tickets_available>0
    }
  },
    methods: {
      validateSeats(){
      if(this.ticket.seats > this.ticket.tickets_available) {
        this.invalid_msg = "Not Enough Seats Available";
      } else if (this.ticket.seats <= 0) {
        this.invalid_msg = "Seats Need to be more than 1";
      }
      else{
        this.invalid_msg = "";
      }
      
    },
      ticketPrice(){
      this.ticket.price = this.ticket.seats*this.ticket_price 
      return this.ticket.seats*this.ticket_price
    },
      resetBookModal() {
        this.ticket.name = ""
        this.ticket.seats = null
        this.ticket.price = null
      },
    openModal(bvModalEvent){
      bvModalEvent.preventDefault()
      console.log("inside btn")
      console.log('book-show-'+String(this.ticket.show_id))
      this.$bvModal.show(this.modal_id)
    },
    closeModal(bvModalEvent){
      bvModalEvent.preventDefault()
      this.$bvModal.hide(this.modal_id)
    },

    bookShow() {
      // Exit when the form isn't valid
      const formData = new FormData();
      console.log("Show File",this.ticket.show_id)
      // Append the file to the FormData object
      formData.append("name",localStorage.getItem('user_name'));
      // Append other form data to the FormData object
      formData.append("seats", this.ticket.seats);
      formData.append("price", this.ticket.price);
      formData.append("show_id",this.ticket.show_id);
      formData.append("user_id", this.user_id);
      axios
        .post(`http://127.0.0.1:5000/home/book`,formData,{
                headers: { 'x-access-token': localStorage.getItem('token') }
            })
        .then((res) => {
          if(res.data.isSuccess) {
            this.$bvModal.msgBoxOk("Ticket Booked successfully", {
              title: "Confirmation",
              size: "sm",
              buttonSize: "sm",
              okVariant: "success",
              headerClass: "p-2 border-bottom-0",
              footerClass: "p-2 border-top-0",
              centered: true,
            }).then(
              () => {
            this.resetBookModal()
            this.$bvModal.hide(this.modal_id)
            this.$router.go(0);
              }
            )
            
            
          }
        })
        .catch((err) => console.log(err));
      // Hide the modal manually
      this.$nextTick(() => {
        this.resetBookModal();
      });
    },
  },
};
</script>