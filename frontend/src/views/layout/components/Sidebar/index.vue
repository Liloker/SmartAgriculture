<template>
  <div>
    <scroll-bar>
      <div class="topbar" v-if="this.sidebar.opened">智慧农业</div>
      <el-menu
        mode="vertical"
        :show-timeout="200"
        :default-active="$route.path"
        :collapse="isCollapse"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <sidebar-item :routes="routes"></sidebar-item>
      </el-menu>
    </scroll-bar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SidebarItem from './SidebarItem'
import ScrollBar from '@/components/ScrollBar'

export default {
  components: { SidebarItem, ScrollBar },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    routes() {
      return this.$router.options.routes
    },
    isCollapse() {
      return !this.sidebar.opened
    }
  }
}
</script>

<style scoped>
.topbar{
  background-color: #021528;
  font-size:18px;
  font-weight: bold;
  position: fixed;
  top: 0;
  left: 0;
  width: 180px;
  z-index: 999;
  color: #ffffff;
  line-height: 50px;
  height: 50px;
  padding-left: 20px;
}
</style>