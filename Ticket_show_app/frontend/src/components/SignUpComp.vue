<template>
        <div class="py-5 h-100">
      <div class="d-flex justify-content-center align-items-center h-100">
        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
          <b-card class="bg-dark text-white" style="border-radius: 1rem;">
            <b-card-body class="p-5 text-center">
              <div class="mb-md-5 mt-md-4 pb-5">
                <h2 class="fw-bold mb-2 text-uppercase">Sign Up</h2>
                <p class="text-white-50 mb-5">Please enter your Email and password!</p>
<b-form @submit="onSubmit" @reset="onReset">
      <b-form-group id="example-input-group-1" label="Name" label-for="example-input-1">
        <b-form-input
          id="example-input-1"
          name="example-input-1"
          v-model="form.username"
          :state="nameState"
          aria-describedby="input-1-live-feedback"
        ></b-form-input>

        <b-form-invalid-feedback
          id="input-1-live-feedback"
        >This is a required field and must be at least 3 characters.</b-form-invalid-feedback>
      </b-form-group>
      <b-form-group id="example-input-group-2" label="Email" label-for="example-input-2">
        <b-form-input
          id="example-input-2"
          name="example-input-2"
          v-model="form.email"
          :state="emailState"
          aria-describedby="input-2-live-feedback"
        ></b-form-input>
        <b-form-invalid-feedback
          id="input-2-live-feedback"
        >INVALID EMAIL</b-form-invalid-feedback>
      </b-form-group>
        <b-row>
         <b-col sm="6">
          <b-form-group id="example-input-group-3" label="Password" label-for="example-input-3">
          <b-form-input
          id="example-input-3"
          name="example-input-3"
          type = "password"
          v-model="form.password"
          :state="passwordState"
          aria-describedby="input-3-live-feedback"
        ></b-form-input>
        <b-form-invalid-feedback
          id="input-3-live-feedback"
        >Length-6|1 UpperCase|1 LowerCase|1 Number|1 Special</b-form-invalid-feedback>
      </b-form-group>
      </b-col> 
         <b-col sm="6">
          <b-form-group id="example-input-group-4" label="Confirm Password" label-for="example-input-4">
          <b-form-input
          id="example-input-4"
          name="example-input-4"
          type = "password"
          v-model="form.cPassword"
          :state="validateCPasswordState"
          aria-describedby="input-4-live-feedback"
        ></b-form-input>
        <b-form-invalid-feedback
          id="input-4-live-feedback"
        >Password Does Not Match</b-form-invalid-feedback>
      </b-form-group>
         </b-col>
        </b-row>  
        <b-button type="submit" variant="outline-light" class="btn-lg px-5" style="margin-top: 25px;">Sign Up</b-button>
    </b-form>
              </div>
              <div>
                <p class="mb-0">Already have an account? <router-link to="/" class="text-white-50 fw-bold">Sign in</router-link></p>
              </div>
            </b-card-body>
          </b-card>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import { validationMixin } from "vuelidate";
// import axios from 'axios' ;
import {mapActions} from 'vuex'

export default {
    mixins: [validationMixin],
    data() {
      return {
        form : {
          username: '',
          email:'',
          password: '',
          cPassword:''
        },
        nameState: null,
        emailState: null,
        passwordState: null,       
        cPasswordState:null,
      };
    },
    methods: {
      ...mapActions({
        signup : 'signup_action' 
      }),
      onSubmit(event) {
        event.preventDefault()
        
        this.signup(this.form)
        // axios.post('http://127.0.0.1:5000/auth/signup', {
        //   username: this.form.username ,
        //   email: this.form.email,
        //   password: this.form.password ,
        //   cPassword: this.form.cPassword
  
        // }).then(res => {console.log(res)})
      },
      onReset(event) {
        event.preventDefault()
        this.form.email = ''
        this.form.username = ''
        this.form.password=''
        this.form.cPassword=''
    },
      emailValidation(email)
      {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        console.log(re.test(email))
        return re.test(email)
            },
      validatePassword(password) {
            const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/
            return re.test(password)
      },
    },
    watch: {
        "form.username": function (val) {
            if (val.length > 2) {
                this.nameState = true
            } else {
                this.nameState = false
            }
        },
        "form.email": function () {
            if (this.emailValidation(this.form.email)) {
                this.emailState = true
            } else {
                this.emailState = false
            }
        },
        "form.password": function () {
            if (this.validatePassword(this.form.password)) {
                this.passwordState = true
            } else {
                this.passwordState = false
            }
        },
    },
    computed:{
      validateCPasswordState() {
            if (this.form.cPassword.length === 0) {
                return null
            }
            return this.form.password === this.form.cPassword ? true : false
        },
    }
  };
  </script>
  
  <style scoped>
.container {
  max-width: 400px;
  margin: 10 auto;
  padding: 20px;
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 5px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.b-form-group {
  margin-bottom: 20px;
}

.b-button {
  width: 100%;
}
</style>

  