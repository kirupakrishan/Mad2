<template>
  <div>
  <div v-if="loading">
    <b-spinner></b-spinner>
  </div>
  <div v-else>        
    <div style="margin-top: 10px;" v-for="venue in venues" :key="venue.id">
      <div v-if="!(Object.entries(shows[venue.id]).length === 0)">
        <div class="venue-header">
      <b-row>
        <b-col md="3" class="venue-header-col">
          <p class="venue-input">{{venue.name.toUpperCase() }}</p>
        </b-col>
        <b-col md="3" class="venue-header-col">
          <p class="venue-input">{{ venue.location.toUpperCase() }}</p>  
        </b-col>
        <b-col md="3" class="venue-header-col">
          <p class="venue-input">Capacity : {{ venue.capacity}}</p>
        </b-col>
      </b-row>
    </div>
    <div class="scroll-container">
      <ul  style="max-width:340px;" class="scroll-content">
        <li v-for="show in shows[venue.id]" :key="show.id"  class ="scroll-item">
          <UserMovieCardComp  :show="show" :key="show.id"/>
        </li> 
      </ul>
    </div>
  </div>
 
</div>
       
  </div>
  </div>
  </template>
  <script>
  // import { Carousel, Navigation, Slide } from 'vue-carousel'

import { mapActions, mapGetters } from 'vuex';
import UserMovieCardComp from './UserMovieCardComp.vue'
  export default ({
    components: {
      UserMovieCardComp,
    },
    data(){
      return {
        search:'',
      }
    },
     mounted() {
      this.getVenues();
    },
    computed:{
      ...mapGetters({
        venues : 'venues',
        shows:'shows',
        loading:'is_loading'
      })
    },
    methods :
    {
      ...mapActions({
        getVenues:'getVenues_action',
      }),
  }
  
  })
  </script>
  <style>
  .scroll-container {
  width: 100%; /* Set the desired width of the container */
}

.scroll-content {
  display: flex; /* Ensure the list items are in a row */
  padding: 0;
  margin: 0;
  list-style: none;
  white-space: nowrap; /* Prevent wrapping of items to a new line */
}

.scroll-item {
  /* Add your desired styles for the items */
  padding: 10px;
  margin: 5px;
  background-color: #f0f0f0;
}
  .venue-header{
    margin: 0px 10px; 
    background: rgb(207, 230, 245);
    border-radius: 10px;
  }
  .venue-header-col{
    margin: 5px 0px;
    place-items: center;
  }
  .venue-input{
    margin:0px ;
    font-size: x-large;
  }
  
  </style>