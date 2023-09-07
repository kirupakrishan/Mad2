<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand to="/home">{{ username }}</b-navbar-brand>
    <b-collapse id="nav-collapse" is-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>User</em>
          </template>
          <b-dropdown-item to="/bookings">Bookings</b-dropdown-item>
          <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-button v-b-toggle.filter style="border-radius: 50%; height:30px; width:30px; vertical-align:middle;"><b-icon icon="filter" shift-v="2" shift-h="-6.7" style="height: 30px; width: 30px; color: white;"></b-icon></b-button>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  <b-sidebar id="filter" title="Filter Movies" width="400px" backdrop-variant="dark" backdrop right shadow>
    <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="location"
        label="Location:"
        label-for="location"
      >
        <b-form-input
          id="location"
          v-model="form.location"
          type="text"
          placeholder="Enter Location"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="show-label" label="Show Name:" label-for="show">
        <b-form-input
          id="show"
          v-model="form.show"
          placeholder="Enter Show Name"
        ></b-form-input>
      </b-form-group>
      <b-form-group id="show-rating-label" label="Show Rating:" label-for="rating">
        <b-form-rating id="rating" v-model="form.rating"></b-form-rating>
      </b-form-group>
      
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
  </b-sidebar>
</div>
</template>

<script>
import {mapActions} from 'vuex'
  export default {
    data() {
      return {
        username : localStorage.getItem('user_name'),
        form:{
        location:null,
        show:null,
        rating:null
        },
        show: true,
      }
    },
    methods: {
      ...mapActions({
        logout:'logout_action',
        getVenues:'getVenues_action',
        getSearch:'getSearch_action'
      }),
      onSubmit(event) {
        event.preventDefault()
        this.getSearch(this.form)
        this.$emit('update')
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.location=null,
        this.form.show=null,
        this.form.rating=null
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.getVenues()
          this.show = true
        })
      }
    }
  }
</script>


