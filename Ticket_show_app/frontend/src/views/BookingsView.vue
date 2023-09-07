<template>
    <div>
<UserNavBarComp></UserNavBarComp>
<UserBookingsComp></UserBookingsComp>
    </div>

</template>

<script>
import UserNavBarComp from '@/components/UserNavBarComp.vue';
import UserBookingsComp from '@/components/UserBookingsComp.vue';

export default {
    components : {UserNavBarComp,UserBookingsComp}
};
</script>

<style>

</style>