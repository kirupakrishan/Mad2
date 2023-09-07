<template>
<div>
<div v-if="loading">
  <b-spinner></b-spinner>
</div>
<div v-else>
  <div style="margin-top: 10px;" v-for="venue in venues" :key="venue.id">
  <div class="venue-header">
    <b-row>
      <b-col md="3" class="venue-header-col">
        <p class="venue-input">{{ venue.name.toUpperCase() }}</p>
      </b-col>
      <b-col md="3" class="venue-header-col">
        <p class="venue-input">{{ venue.location.toUpperCase() }}</p>  
      </b-col>
      <b-col md="3" class="venue-header-col">
        <p class="venue-input">Capacity : {{ venue.capacity}}</p>
      </b-col>
      <b-col md="3" class="venue-header-col">
        <p class="venue-input">VID:{{ venue.id }}</p>
      </b-col>
    </b-row>
  </div>
  <Carousel v-if="shows[venue.id]" :items-to-show="4" :wrap-around="true" style="margin: 10px;">
    <Slide v-for="show in shows[venue.id]" :key="show.sid" style="max-width:340px;">
      <AdminMovieCardComp :show="show"/>
    </Slide>
    <template #addons>
      <Navigation />
    </template>
  </Carousel>
</div>

</div>
</div>
</template>
<script>
import { Carousel, Navigation, Slide } from 'vue-carousel'
import axios from 'axios'
import AdminMovieCardComp from './AdminMovieCardComp.vue'
export default ({
  components: {
    Carousel,
    Slide,
    Navigation,
    AdminMovieCardComp,
  },
  data(){
    return {
      venues : [],
      shows:{},
      loading : true
    }
  },
   mounted() {
    this.getVenues();
  },
  methods :
  {
   async getVenues(){
       axios.get("http://127.0.0.1:5000/admin/venue/getall",{
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then(res => {
        this.venues = res.data.venues
        this.getShows();
        })

    },
    async getShows() {
      for(let venue in this.venues){
        try {
          const res = await axios.get(`http://127.0.0.1:5000/admin/show/getall/${venue}`,{
                headers: { 'x-access-token': localStorage.getItem('token') }
            })
          this.shows[venue] = res.data.shows
          console.log(this.shows)
        } catch(err) {
        console.log(err)
      }
      }
      this.loading = false 
  }
}

})
</script>
<style>
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
