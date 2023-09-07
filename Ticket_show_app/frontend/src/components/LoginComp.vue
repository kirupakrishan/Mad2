<template >
      <div class="d-flex justify-content-center align-items-center">
        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
          <b-card class="bg-dark text-white" style="border-radius: 1rem;">
            <b-card-body class="p-5 text-center">
              <div class="mb-md-5 mt-md-4 pb-5">
                <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
                <p class="text-white-50 mb-5">Please enter your login and password!</p>
                <b-form  @submit="onSubmit" @reset="onReset">
                  <b-form-group
                  id="email-group"
                  label="Email"
                  label-for="typeEmailX"
                >
                  <b-form-input
                    id="typeEmailX"
                    v-model="form.email"
                    type="email"
                    class="form-control-lg"
                    required
                  ></b-form-input>
                </b-form-group>

                <b-form-group
                  id="password-group"
                  label="Password"
                  label-for="typePasswordX"
                >
                  <b-form-input
                    id="typePasswordX"
                    v-model="form.password"
                    type="password"
                    class="form-control-lg"
                    required
                    ></b-form-input>
                </b-form-group>

                <b-button variant="outline-light" type = "submit" class="btn-lg px-5" style="margin-top: 25px;">Login</b-button>
              </b-form>
              </div>
              <div>
                <p class="mb-0">Don't have an account? <router-link to="/Signup" class="text-white-50 fw-bold">Sign Up</router-link></p>
              </div>
            </b-card-body>
          </b-card>
        </div>
      </div>
</template>

  

<script>
import {mapActions} from 'vuex'
  export default {
    data() {
      return {
        form : {
          email: '',
          password: ''
        }
        
      };
    },
    methods: {
      ...mapActions({
            login: 'login_action'
        }),
      onSubmit(event) {
        event.preventDefault()
        let payload = new FormData()
        payload.append('email',this.form.email)
        payload.append('password',this.form.password)
        this.login(payload)
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.name = ''
    }
  }
  };
  </script>
  
  <style scoped>
h2 {
  text-align: center;
  margin-bottom: 20px;
}

.b-from-group {
  margin-bottom: 200px;
}
.b-button {
  width: 100%;
}
  </style>
  