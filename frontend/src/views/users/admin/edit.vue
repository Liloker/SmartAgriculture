<template>
  <admin-detail :isEdit="true"></admin-detail>
</template>
<script>
import AdminDetail from "./components/AdminDetail";
export default {
  name: "addAdmin",
  components: { AdminDetail }
};
</script>
<style scoped></style>
