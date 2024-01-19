<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'App'
  }
</script>

<style>
.link{
  cursor: pointer;
  color: #218FFF;
}

.el-menu--horizontal>.el-menu-item.is-active{
  color: #409EFF;
}

.el-menu--horizontal>.el-menu-item{
  color: #409EFF;
}

.el-menu--horizontal>.el-submenu .el-submenu__title{
  color: #409EFF;
}

.el-menu--horizontal .el-menu .el-menu-item, .el-menu--horizontal .el-menu .el-submenu__title{
  color: #409EFF;
}
</style>
