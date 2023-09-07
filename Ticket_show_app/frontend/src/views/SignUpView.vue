<template>
          <SignUpComp @signup-success="handleSignupSuccess"></SignUpComp>
  </template>
  
  <script>
  import SignUpComp from '@/components/SignUpComp.vue';
  
  export default {
    components: {
      SignUpComp
    },
    methods: {
      handleLoginSuccess() {
        // Handle login success, e.g., redirect to dashboard
        console.log('Login successful!');
      },
      handleSignupSuccess() {
        // Handle signup success, e.g., display a success message
        console.log('Signup successful!');
      }
    }
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  