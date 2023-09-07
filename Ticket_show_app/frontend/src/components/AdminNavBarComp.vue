<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <router-link to="/admin/dashboard" style="font-size:20px; color: whitesmoke; margin: 10px 3px;">ADMIN</router-link>
        <b-collapse id="nav-collapse" is-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-navbar-nav>
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>Report</em>
            </template>
            <b-dropdown-item ><router-link to="/admin/report" style="color:black">Report</router-link></b-dropdown-item>
            <b-dropdown-item @click="export_CSV">Download Csv</b-dropdown-item>
          </b-nav-item-dropdown>
          </b-navbar-nav>

          <b-navbar-nav>
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>Venue</em>
            </template>
            <b-dropdown-item v-b-modal.add-venue>Add Venue</b-dropdown-item>
            <b-dropdown-item v-b-modal.edit-venue>Edit Venue</b-dropdown-item>
            <b-dropdown-item v-b-modal.delete-venue>Delete Venue</b-dropdown-item>
          </b-nav-item-dropdown>
          </b-navbar-nav>
          <template>
            <div>
              <b-modal
                id="add-venue"
                ref="modal"
                title="Submit Venue Details"
                @show="resetModal"
                @hidden="resetModal"
                @ok="handleOk"
              >
                <form ref="form" @submit.stop.prevent="handleSubmit">
                  <b-form-group
                  id="vname-input"
                  label="Enter Venue Name"
                  label-for="vname"
                  :invalid-feedback="vnameinvalidFeedback"
                  :state="vnamestate"
                >
                  <b-form-input id="vname" v-model="venue.vname" :state="vnamestate" trim required></b-form-input>
                </b-form-group>
                <b-form-group
                  id="vlocation-input"
                  label="Enter Venue Location"
                  label-for="vlocation"
                  :invalid-feedback="vlocationinvalidFeedback"
                  :state="vlocationstate"
                >
                  <b-form-input id="vlocation" v-model="venue.vlocation" :state="vlocationstate" trim required></b-form-input>
                </b-form-group>
                <b-form-group
                  id="vcapacity-input"
                  label="Enter Venue Capacity"
                  label-for="vcapacity"
                  :invalid-feedback="vcapacityinvalidFeedback"
                  :state="vcapacitystate"
                >
                  <b-form-input id="vcapacity" v-model="venue.vcapacity" :state="vcapacitystate" trim required></b-form-input>
                </b-form-group>
                </form>
              </b-modal>
              </div>
              </template>
              <template>
            <div>
              <b-modal
                id="edit-venue"
                ref="modal"
                title="Enter Venue ID"
                @shown="resetEditModal"
                @hidden="resetModal"
              >
              <template #modal-footer>
                  <b-button size="sm" variant="primary" v-if="toggleGetEditState" @click="getVenueDetails">
                    Get Details
                  </b-button>
                  <b-button size="sm" variant="primary" v-else @click="updateVenueDetails">
                    Update Details
                  </b-button>
                </template>
                <form ref="form" @submit.stop.prevent="handleSubmit">
                  <b-form-group
                  id="vid-input"
                  label="Enter Venue ID"
                  label-for="vid"
                >
                  <b-form-input id="vid" v-model="venue.vid" trim required></b-form-input>
                </b-form-group>
                  
                  <b-form-group
                  id="vname-input"
                  label="Enter Venue Name"
                  label-for="vname"
                  :invalid-feedback="vnameinvalidFeedback"
                  :state="vnamestate"
                  v-if="!toggleGetEditState"
                >
                  <b-form-input id="vname" v-model="venue.vname" :state="vnamestate" trim></b-form-input>
                </b-form-group>
                <b-form-group
                  id="vlocation-input"
                  label="Enter Venue Location"
                  label-for="vlocation"
                  :invalid-feedback="vlocationinvalidFeedback"
                  :state="vlocationstate"
                  v-if="!toggleGetEditState"
                >
                  <b-form-input id="vlocation" v-model="venue.vlocation" :state="vlocationstate" trim ></b-form-input>
                </b-form-group>
                <b-form-group
                  id="vcapacity-input"
                  label="Enter Venue Capacity"
                  label-for="vcapacity"
                  :invalid-feedback="vcapacityinvalidFeedback"
                  :state="vcapacitystate"
                  v-if="!toggleGetEditState"
                >
                  <b-form-input id="vcapacity" v-model="venue.vcapacity" :state="vcapacitystate" trim ></b-form-input>
                </b-form-group>
                </form>
              </b-modal>
              </div>
              </template>
              <template>
            <div>
              <b-modal
                id="delete-venue"
                ref="modal"
                title="Delete Venue"
                @show="resetModal"
                @hidden="resetModal"
                @ok="deleteVenueDetails"
              >
                <form ref="form" @submit.stop.prevent="handleSubmit">
                  <b-form-group
                  id="vid-input"
                  label="Enter Venue ID"
                  label-for="vid"
                >
                  <b-form-input id="vid" v-model="venue.vid" trim required></b-form-input>
                </b-form-group>
                </form>
              </b-modal>
              </div>
              </template>
              <b-navbar-nav>
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>Show</em>
            </template>
            <b-dropdown-item v-b-modal.add-show>Add Show</b-dropdown-item>
            <b-dropdown-item v-b-modal.edit-show>Edit Show</b-dropdown-item>
            <b-dropdown-item v-b-modal.delete-show>Delete Show</b-dropdown-item>
          </b-nav-item-dropdown>
          </b-navbar-nav>
          <template>
            <div>
              <b-modal
                id="add-show"
                ref="modal"
                title="Submit Show Details"
                @show="resetShowModal"
                @hidden="resetShowModal"
                @ok="createShow"
              >
                <form ref="form" @submit.stop.prevent="handleSubmit">
                  <b-form-group
                  id="vid-input"
                  label="Enter Venue ID"
                  label-for="vid"
                >
                  <b-form-input id="vid" v-model="show.vid" trim required></b-form-input>
                </b-form-group>
                  <b-form-group
                  id="sname-input"
                  label="Enter Show Name"
                  label-for="sname"
                  :invalid-feedback="snameinvalidFeedback"
                  :state="snameState"
                >
                  <b-form-input id="sname" v-model="show.sname" :state="snameState" trim required></b-form-input>
                </b-form-group>
                <b-form-group
                  id="stags-input"
                  label="Enter Show Tags"
                  label-for="stags"
                >
                <b-form-tags input-id="stags" separator=" ,;" v-model="show.stags" remove-on-delete></b-form-tags>                </b-form-group>
                <b-form-group
                  id="rating-input"
                  label="Enter Show Rating"
                  label-for="srating"
                  :invalid-feedback = "sratinginvalidFeedback"
                  :state = "sratingstate"
                >
                  <b-form-input id="srating" v-model="show.rating" :state = "sratingstate" trim required></b-form-input>
                </b-form-group>
                <b-form-file
                      accept = "image/*"
                      v-model="show.simg"
                      :state="Boolean(show.simg)"
                      placeholder="Upload Show Poster..........."
                      drop-placeholder="Drop file here..."
                    ></b-form-file>
                <b-form-group
                  id="stime-input"
                  label="Enter Show DateTime"
                  label-for="stime"
                >
                <b-form-datepicker id="sdate" v-model="show.sdate" class="mb-2"></b-form-datepicker>
                <b-form-timepicker v-model="show.stime" locale="en"></b-form-timepicker>
                </b-form-group>
                </form>
              </b-modal>
              </div>
              </template>
              <template>
            <div>
              <b-modal
                id="edit-show"
                ref="modal"
                title="Submit Show Details"
                @show="resetModal"
                @hidden="resetShowModal"
              >
              <template #modal-footer>
                  <b-button size="sm" variant="primary" v-if="toggleGetEditState" @click="getShowDetails">
                    Get Details
                  </b-button>
                  <b-button size="sm" variant="primary" v-else @click="updateShowDetails">
                    Update Details
                  </b-button>
                </template>
                <form ref="form" @submit.stop.prevent="handleSubmit">
                  <b-form-group
                  id="vid-input"
                  label="Enter Venue ID"
                  label-for="vid"
                  v-if="!toggleGetEditState"
                >
                <b-form-input id="vid" v-model="show.vid" trim required></b-form-input>
                </b-form-group>
                <b-form-group
                  id="sid-input"
                  label="Enter Show ID"
                  label-for="sid"
                >
                  <b-form-input id="sid" v-model="show.sid" trim required></b-form-input>
                </b-form-group>
                  <b-form-group
                  id="sname-input"
                  label="Enter Show Name"
                  label-for="sname"
                  :invalid-feedback="snameinvalidFeedback"
                  :state="snameState"
                  v-if="!toggleGetEditState"
                >
                  <b-form-input id="sname" v-model="show.sname" :state="snameState" trim required></b-form-input>
                </b-form-group>
                <b-form-group
                  id="stags-input"
                  label="Enter Show Tags"
                  label-for="stags"
                  v-if="!toggleGetEditState"
                >
                <b-form-tags input-id="stags" separator=" ,;" v-model="show.stags" remove-on-delete></b-form-tags>                </b-form-group>
                <b-form-group
                  id="rating-input"
                  label="Enter Show Rating"
                  label-for="srating"
                  :invalid-feedback = "sratinginvalidFeedback"
                  :state = "sratingstate"
                  v-if="!toggleGetEditState"
                >
                  <b-form-input id="srating" v-model="show.rating" :state = "sratingstate" trim required></b-form-input>
                </b-form-group>
                <b-form-file
                      accept = "image/*"
                      v-model="show.simg"
                      :state="Boolean(show.simg)"
                      placeholder="Upload Show Poster..........."
                      drop-placeholder="Drop file here..."
                      v-if="!toggleGetEditState"
                    ></b-form-file>
                    <span v-if="!toggleGetEditState" >Show Time : {{ this.show.sdate}} {{ this.show.stime }}</span>  
                <b-form-group
                  id="stime-input"
                  label="Enter Show DateTime"
                  label-for="stime"
                  v-if="!toggleGetEditState"
                >
                <b-form-datepicker id="sdate" value="show_date" v-model="show.sdate" class="mb-2"></b-form-datepicker>
                <b-form-timepicker value="show_time" v-model="show.stime" locale="en"></b-form-timepicker>
                </b-form-group>
                </form>
              </b-modal>
              </div>
              </template>
              <template>
            <div>
              <b-modal
                id="delete-show"
                ref="modal"
                title="Delete Show"
                @show="resetModal"
                @hidden="resetModal"
                @ok="deleteShowDetails"
              >
                <form ref="form" @submit.stop.prevent="handleSubmit">
                  <b-form-group
                  id="sid-input"
                  label="Enter Show ID"
                  label-for="sid"
                >
                  <b-form-input id="sid" v-model="show.sid" trim required></b-form-input>
                </b-form-group>
                </form>
              </b-modal>
              </div>
              </template>

              <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>User</em>
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
  </template>


<script>
import axios from 'axios'
import {mapActions} from 'vuex'
export default{
  data(){
    return {

     venue :{ 
      vid : null,
      vname: '',
      vlocation:'',
      vcapacity:null,
    },
    show : {
      sid:null,
      vid:null,
      simg:null,
      sname:'',
      stags:[],
      sdate:null,
      stime:null,
      rating:0,
    },
    toggleGetEditState:true,
    vidpresentState:false,
    

  }
    
  },
  methods: {
    ...mapActions({
      logout:'logout_action'
    }),
      resetModal() {
        this.venue.vid=null
        this.venue.vname = ''
        this.venue.vlocation = ''
        this.venue.vcapacity=null
        this.$bvModal.hide('add-venue')
      },
      resetEditModal(){
        this.toggleGetEditState = true ;
      },
      resetShowModal() {
        this.show.sid=null
        this.show.vid=null
        this.show.simg=null
        this.show.sname=''
        this.show.stags=[]
        this.show.sdate=null
        this.show.stime=null
        this.show.rating=0
        this.resetEditModal()
      },
      handleOk(bvModalEvent) {
        // Prevent modal from closing
        bvModalEvent.preventDefault()
        // Trigger submit handler
        this.handleSubmit()
      },
      handleSubmit() {
        // Exit when the form isn't valid
        if (!this.checkFormValidity) {
          return
        }
        axios.post('http://127.0.0.1:5000/admin/venue/create', {
          vname: this.venue.vname ,
          vlocation: this.venue.vlocation,
          vcapacity: this.venue.vcapacity ,
        },{
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then(() => {          
          this.$bvModal.msgBoxOk('Data was submitted successfully', {
          title: 'Confirmation',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        }) 
        })
        // Hide the modal manually
        this.$nextTick(() => {
          this.resetModal()
          this.$emit('remount')
        })
      },
      async export_CSV() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/admin/reports/export',{
                headers: { 'x-access-token': localStorage.getItem('token') },
                responseType: 'blob'});
        console.log(response.status)
        console.log(response.data)
        // Create a Blob URL for the CSV data
        const blob = new Blob([response.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);

        // Create a link element and simulate a click to trigger download
        const link = document.createElement('a');
        link.href = url;
        link.download = 'venues.csv';
        link.click();
        // Clean up the Blob URL
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Error exporting CSV:', error);
      }
    },
     async getVenueDetails(bvModalEvent) {
        bvModalEvent.preventDefault()
        // Exit when the form isn't valid
        await axios.get(`http://127.0.0.1:5000/admin/venue/get/${this.venue.vid}`,{
                headers: { 'x-access-token': localStorage.getItem('token') }
            })
        .then(res => { 
          this.venue.vname = res.data.venue['name'] ,
          this.venue.vlocation = res.data.venue['location'],
          this.venue.vcapacity = res.data.venue['capacity'],
          this.toggleGetEdit()
        }).catch(err => console.log(err))
      },
      async updateVenueDetails(bvModalEvent) {
        this.toggleGetEdit()
        bvModalEvent.preventDefault()
        if (!this.checkFormValidity) {
          return
        }
        // Exit when the form isn't valid
        await axios.put(`http://127.0.0.1:5000/admin/venue/update/${this.venue.vid}`,{'vname': this.venue.vname ,
          'vlocation': this.venue.vlocation,
          'vcapacity': this.venue.vcapacity ,},{
                headers: { 'x-access-token': localStorage.getItem('token') }
            },
)
        .then(() => {  
          this.$bvModal.msgBoxOk('Data Was Updated Successfully', {
          title: 'Confirmation',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        })
        }).catch(err => console.log(err))
        this.resetModal()
        this.$bvModal.hide('edit-venue')
        this.$emit('remount')
      },
      deleteVenueDetails(bvModalEvent) {
        bvModalEvent.preventDefault()
        this.$bvModal.msgBoxConfirm('Please confirm that you want to delete everything.', {
          title: 'Please Confirm',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: 'YES',
          cancelTitle: 'NO',
          footerClass: 'p-2',
          hideHeaderClose: false,
          centered: true
        })
          .then( res => {
            if(res)
            {
              axios.delete(`http://127.0.0.1:5000/admin/venue/delete/${this.venue.vid}`,{
                headers: { 'x-access-token': localStorage.getItem('token') }
            })
        .then(() => {  
          this.$bvModal.msgBoxOk('Data Was Deleted Successfully', {
          title: 'Confirmation',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        })
        })
          }
          this.resetModal()
          this.$bvModal.hide('delete-venue')
          this.$emit('remount')
          }
          )
          .catch(err => {
            console.log(err)
          })
        },
        createShow() {
              // Exit when the form isn't valid
        const formData = new FormData();
        const showTime = new Date(this.show.sdate + ' ' + this.show.stime);
        // Append the file to the FormData object
        formData.append('simg', this.show.simg);
        // Append other form data to the FormData object
        formData.append('vid', this.show.vid);
        formData.append('sname', this.show.sname);
        formData.append('stags', this.show.stags);
        formData.append('show_time',showTime.toISOString());
        formData.append('rating', this.show.rating);
        axios.post('http://127.0.0.1:5000/admin/show/create', 
        formData,{headers: {
          'Content-Type': 'multipart/form-data',
          'x-access-token': localStorage.getItem('token') }}).then(res => {       
          if(res.data.vidAbsent)
          {
          this.$bvModal.msgBoxOk('Given Venue ID is Not Present', {
          title: 'ERROR',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        })  
          }
        else{
          this.$bvModal.msgBoxOk('Data was submitted successfully', {
          title: 'Confirmation',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        })
        }
           
        }).catch(err => console.log(err))
        // Hide the modal manually
        this.$nextTick(() => {
          this.resetShowModal()
          this.$emit('remount')
        })
      },
      async getShowDetails(bvModalEvent) {
        bvModalEvent.preventDefault()
        // Exit when the form isn't valid
        await axios.get(`http://127.0.0.1:5000/admin/show/get/${this.show.sid}`,{
                headers: { 'x-access-token': localStorage.getItem('token') }
            })
        .then(res => { 
          console.log(res.data.show)
          this.show.vid = res.data.show['venue_id'],
          this.show.sname = res.data.show['name'] ,
          this.show.stags = res.data.show['tags'].split(','),
          this.show.rating = res.data.show['rating'],
          this.show.stime = res.data.show['stime']
          this.show.sdate = res.data.show['sdate']
          this.toggleGetEdit()
        }).catch(err => console.log(err))
        console.log(this.show)
      },
      async updateShowDetails(bvModalEvent) {
        this.toggleGetEdit()
        bvModalEvent.preventDefault()
        const form = new FormData()
        const showTime = new Date(this.show.sdate + ' ' + this.show.stime);
        form.append('vid',this.show.vid)
        form.append('sname',this.show.sname)
        form.append('stags',this.show.stags)
        form.append('srating',this.show.rating)
        form.append('simg',this.show.simg)
        form.append('stime',showTime.toISOString())
        // Exit when the form isn't valid
        await axios.put(`http://127.0.0.1:5000/admin/show/update/${this.show.sid}`,
          form,{
                headers: { 'x-access-token': localStorage.getItem('token'),
                'Content-Type': 'multipart/form-data', }
            },)
        .then(() => {  
          this.$bvModal.msgBoxOk('Data Was Updated Successfully', {
          title: 'Confirmation',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        })
        }).catch(err => console.log(err))
        this.resetModal()
        this.$bvModal.hide('edit-show')
        this.$emit('remount')
      },
      deleteShowDetails(bvModalEvent) {
        bvModalEvent.preventDefault()
        this.$bvModal.msgBoxConfirm('Please confirm that you want to delete everything.', {
          title: 'Please Confirm',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'danger',
          okTitle: 'YES',
          cancelTitle: 'NO',
          footerClass: 'p-2',
          hideHeaderClose: false,
          centered: true
        })
          .then( res => {
            if(res)
            {
              axios.delete(`http://127.0.0.1:5000/admin/show/delete/${this.show.sid}`,{
                headers: { 'x-access-token': localStorage.getItem('token') }
            })
        .then(() => {  
          this.$bvModal.msgBoxOk('Data Was Deleted Successfully', {
          title: 'Confirmation',
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        })
        })
          }
          this.resetShowModal()
          this.$bvModal.hide('delete-show')
          this.$emit('remount')
          }
          )
          .catch(err => {
            console.log(err)
          })
        },
      toggleGetEdit(){
      this.toggleGetEditState = !this.toggleGetEditState
  },
},
computed : {
  checkFormValidity(){
    return (this.vlocationstate && this.vnamestate && this.vcapacitystate)
  },
  snameState(){
      return this.show.sname.length >=4
  },
  snameinvalidFeedback() {
        if (this.show.sname.length > 0) {
          return 'Enter at least 4 characters.'
        }
        return 'Please enter something.'
      },
  vlocationstate() {
        return this.venue.vlocation.length >= 4
      },
      vlocationinvalidFeedback() {
        if (this.venue.vlocation.length > 0) {
          return 'Enter at least 4 characters.'
        }
        return 'Please enter something.'
      },
      vnamestate() {
        return this.venue.vname.length >= 4
      },
      vnameinvalidFeedback() {
        if (this.venue.vname.length > 0) {
          return 'Enter at least 4 characters.'
        }
        return 'Please enter something.'
      },
      vcapacitystate() {
        return this.venue.vcapacity >= 50
      },
      vcapacityinvalidFeedback() {
        if (this.venue.vcapacity < 50) {
          return 'Minimum capacity is 50'
        }
        return 'Please enter something.'
      },
      sratingstate() {
        return this.show.rating <= 5
      },
      sratinginvalidFeedback() {
        if (this.show.rating > 5) {
          return 'Maximum rating is 5'
        }
        return 'Please enter movie rating.'
      },
      vidinvalidFeedback() {
        if (this.vidpresentState) {
          return 'Given Venue ID is not Present'
        }
        return 'Please enter Venue ID.'
      },
    }

}
</script>
