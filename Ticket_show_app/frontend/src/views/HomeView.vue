<template>
    <div>
    <UserNavBarComp @update="remount"></UserNavBarComp>
    <UserMovieComp :key="userMovieCompKey"></UserMovieComp>
    
    </div>
    

</template>

<script>
import UserNavBarComp from '@/components/UserNavBarComp.vue';
import UserMovieComp from '@/components/UserMovieComp.vue';

export default {
    components : {UserNavBarComp,UserMovieComp},
    data(){
        return{
            userMovieCompKey:1
        }
    },
    methods:{
        remount(){
            this.userMovieCompKey++;
        }
    }
};
</script>

<style>

</style>