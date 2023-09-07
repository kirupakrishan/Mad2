<template>
  <b-card
    :title= "show.name"
    :img-src="`http://127.0.0.1:5000/admin/show/get/img/${show.id}`"
    img-height="300px"
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 300px;"
    class="mb-2"
  >
  <b-container>
<b-row>
    <b-col style=" padding: 5px;">Time:{{ show.time }}</b-col>
    <b-col style="padding: 5px;">Date:{{ show.date }}</b-col>
  </b-row>  
   <b-row>
    <b-col>VID:{{show.venue_id}}</b-col>
    <b-col>SID:{{show.id}} </b-col>
  </b-row>  
  <b-row>
  <b-row>
    <b-col>{{show.tickets_available}}/{{show.tickets_available+show.tickets_booked}} Tickets Available</b-col>
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
  </b-card>
</template>


<script>
export default {
  props:['show'],
  data() {
    return {
      value: [],
      name: "",
      nameState: null,
      rating : this.show.rating,
      submittedNames: [],
    };
  },
  mounted(){
  },
  methods: {
        getImageSrc() {
            return 
        },
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.nameState = valid;
      return valid;
    },
    resetModal() {
      this.name = "";
      this.nameState = null;
      this.$bvModal.hide("edit-movie");
    },
    handleOk(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      // Push the name to submitted names
      this.submittedNames.push(this.name);
      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide("edit-movie");
      });
    },
    showMsgBoxTwo() {
      this.boxTwo = "";
      this.$bvModal
        .msgBoxConfirm("Please confirm that you want to delete everything.", {
          title: "Please Confirm",
          size: "sm",
          buttonSize: "sm",
          okVariant: "danger",
          okTitle: "YES",
          cancelTitle: "NO",
          footerClass: "p-2",
          hideHeaderClose: false,
          centered: true,
        })
        .then((value) => {
          this.boxTwo = value;
        })
        .catch((err) => {
          console.error(err);
        });
      },
  },
};
</script>