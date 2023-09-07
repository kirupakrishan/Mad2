<template>
  <div>
    <LoginComp class="vh-100 gradient-custom">
  </LoginComp>
  </div>
          
  </template>
  
  <script>
  import LoginComp from '@/components/LoginComp.vue';

  export default {
    components: {
      LoginComp
    },
  };
  </script>
  
  <style scoped>
.container {
  max-width: 400px;
  margin: 0px ;
  padding: 0px;
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.gradient-custom {
/* fallback for old browsers */
background: #6a11cb;

/* Chrome 10-25, Safari 5.1-6 */
background: -webkit-linear-gradient(to right, rgba(106, 17, 203, 1), rgba(37, 117, 252, 1));

/* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
background: linear-gradient(to right, rgba(106, 17, 203, 1), rgba(37, 117, 252, 1))
}
  </style>
  