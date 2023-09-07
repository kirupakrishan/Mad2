<template>
    <div>
<AdminNavBarComp @remount="update"></AdminNavBarComp>
<router-view :key="keyval"></router-view>
    </div>

</template>

<script>
import AdminNavBarComp from '@/components/AdminNavBarComp.vue';
export default {
    components : {AdminNavBarComp},
    data(){
        return{
            keyval:1
        }
    },
    methods:{
        update(){
            console.log('updating')
            this.keyval++;
        }
    }

};
</script>

<style>

</style>