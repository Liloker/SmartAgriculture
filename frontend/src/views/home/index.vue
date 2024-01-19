<template>
  <div class="app-container">
    <div class="zonglan">系统运行总览</div>
    <div class="total-layout">
      <el-row :gutter="24">
        <el-col :span="6" >
          <div class="title">累计客户数</div>
          <div class="content">{{ chat.memberCount }}</div>
        </el-col>
        <el-col :span="6">
          <div class="title">今日新增顾客数</div>
          <div class="content">{{ chat.memberTodayIncrement }}</div>
        </el-col>
      </el-row>
    </div>
    <div id="myChart" style="width:100%; height:600px; margin-top:20px;">
      <div class="axis-content">
        <div
          id="allChart"
          class="axismain"/>
      </div>
    </div>
  </div>
</template>

<script>
import store from "@/store";
import echarts from 'echarts'
import 'echarts/map/js/china.js'
import { str2Date } from "@/utils/date";
import request from "@/utils/request";
import { chart } from "@/api/chart";

export default {
  name: "home",
  data() {
    return {
      store:store,
      tokens: store.state.user.roles,
      loading: false,
      dataEmpty: false,
      allChart: null,
      chat: {
        memberCount: 0,
        memberTodayIncrement: 0,
      }
    };
  },
  created() {
    this.chart();
  },
  methods: {
    
    chart() {
      chart().then(res => {
        this.chat = res.data;
      })
    }

  }
};
</script>

<style scoped>
.app-container {
  margin-top: 40px;
  margin-left: 120px;
  margin-right: 120px;
}

.total-layout {
  border: 1px solid #ebeef5;
  border-top: none;
  height: 100px;
  padding: 20px 30px;
}

.title{
  color: #dcdfe6;
  font-size: 12px;
  height: 25px;
  line-height: 25px;
}

.content{
  font-size: 20px;
  height: 30px;
  line-height: 30px;
}

.total-frame {
  border: 1px solid #dcdfe6;
  padding: 20px;
  height: 100px;
}

.total-icon {
  color: #409eff;
  width: 60px;
  height: 60px;
}

.total-title {
  position: relative;
  font-size: 16px;
  color: #909399;
  left: 70px;
  top: -50px;
}

.total-value {
  position: relative;
  font-size: 18px;
  color: #606266;
  left: 70px;
  top: -40px;
}

.un-handle-layout {
  margin-top: 20px;
  border: 1px solid #dcdfe6;
}

.layout-title {
  color: #606266;
  padding: 15px 20px;
  background: #f2f6fc;
  font-weight: bold;
}

.un-handle-content {
  padding: 20px 40px;
}

.un-handle-item {
  border-bottom: 1px solid #ebeef5;
  padding: 10px;
}

.overview-layout {
  margin-top: 20px;
}

.overview-item-value {
  font-size: 24px;
  text-align: center;
}

.overview-item-title {
  margin-top: 10px;
  text-align: center;
}

.out-border {
  border: 1px solid #dcdfe6;
}

.statistics-layout {
  margin-top: 20px;
  border: 1px solid #dcdfe6;
}
.mine-layout {
  position: absolute;
  right: 140px;
  top: 107px;
  width: 250px;
  height: 235px;
}
.address-content {
  padding: 20px;
  font-size: 18px;
}

.zonglan{
  font-size: 16px;
  height: 50px;
  line-height: 50px;
  padding-left: 30px;
  font-weight: bold;
  border: 1px solid #ebeef5;
}

.col{
  padding-left: 40px;
}

.axismain{
  margin: 0 auto;
  margin-top: 100px;
  width: 100%;
  height: 400px;
}
</style>
