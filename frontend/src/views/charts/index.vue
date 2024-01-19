<template>
  <div class="app-container">
    <div class="search">
      <el-card class="filter-container" shadow="never">
        <div style="margin-top: 15px">
          <el-form
            :inline="true"
            :model="listQuery"
            size="small"
            label-width="140px"
          >
            <el-form-item label="大棚编号：">
              <el-select placeholder="请选择" v-model="listQuery.greenhouse_id">
                <el-option 
                  v-for="item in greenhouses"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>

            <el-date-picker
              type="daterange"
              align="right"
              unlink-panels
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              v-model="listQuery.searchDate"
              size="small">
            </el-date-picker>

            <el-form-item style="margin-left:0px;">
            <el-button
              style="float:right"
              type="primary"
              @click="handleSearchList()"
              size="small"
              >查询搜索</el-button
            >
            <el-button
              style="float:right;margin-right: 15px"
              @click="handleResetSearch()"
              size="small"
              >重置</el-button
            >
            </el-form-item>
          </el-form>
        </div>
      </el-card>
    </div>
    
    <div style="display: flex;">

      <el-card class="box-card" style="margin-top: 30px; flex: 1;">
        <div slot="header" class="clearfix">
          <span>空气温度</span>
        </div>
        <div>
          <ve-line 
          :data="datas.chat1"
          height="300px"
          ></ve-line>
        </div>
      </el-card>
      
      <el-card class="box-card" style="margin-top: 30px; flex: 1; margin-left: 20px;">
        <div slot="header" class="clearfix">
          <span>空气湿度</span>
        </div>
        <div>
          <ve-line 
          :data="datas.chat2"
          height="300px"
          ></ve-line>
        </div>
      </el-card>

      <el-card class="box-card" style="margin-top: 30px; flex: 1; margin-left: 20px;">
        <div slot="header" class="clearfix">
          <span>二氧化碳浓度</span>
        </div>
        <div>
          <ve-line 
          :data="datas.chat3"
          height="300px"
          ></ve-line>
        </div>
      </el-card>

    </div>

    
    <div style="display: flex;">

      <el-card class="box-card" style="margin-top: 30px; flex: 1;">
        <div slot="header" class="clearfix">
          <span>光照度</span>
        </div>
        <div>
          <ve-line 
          :data="datas.chat4"
          height="300px"
          ></ve-line>
        </div>
      </el-card>

      <el-card class="box-card" style="margin-top: 30px; flex: 1; margin-left: 20px;">
        <div slot="header" class="clearfix">
          <span>土壤温度</span>
        </div>
        <div>
          <ve-line 
          :data="datas.chat5"
          height="300px"
          ></ve-line>
        </div>
      </el-card>

      <el-card class="box-card" style="margin-top: 30px; flex: 1; margin-left: 20px;">
        <div slot="header" class="clearfix">
          <span>土壤湿度</span>
        </div>
        <div>
          <ve-line 
          :data="datas.chat6"
          height="300px"
          ></ve-line>
        </div>
      </el-card>

    </div>


  </div>
</template>
<script>
import { getChartList, getChartListRealtime, stopChartListRealtime } from "@/api/chart";
import { fetchGreenhouseList } from "@/api/greenhouse";

const defaultListQuery = {
  greenhouse_id: 0,
  start_date: null,
  end_date: null
};

export default {
  name: "orderList",
  data() {
    return {
      listQuery: Object.assign({}, defaultListQuery),
      listLoading: false,
      greenhouses: [],

      datas: {}
    };
  },
  created() {
    this.initWebSocket();
    fetchGreenhouseList().then(res => {
      this.greenhouses = res.data
      defaultListQuery.greenhouse_id = this.greenhouses[0].id
      this.listQuery = {...defaultListQuery}
      this.getListRealtime();
    })
  },
  methods: {

    getListRealtime() {
      this.listLoading = true;
      getChartListRealtime(this.listQuery).then(response => {
        this.listLoading = false;
        this.datas = response.data;
      });
    },

    handleSearchList() {
      this.listLoading = true
      if (this.listQuery.searchDate) {
        console.log("历史");
        stopChartListRealtime()
        this.listQuery.start_date = this.listQuery.searchDate[0]
        this.listQuery.end_date = this.listQuery.searchDate[1]
        getChartList(this.listQuery).then(res => {
          console.log("-----", res.data);
          this.listLoading = false;
          this.datas = res.data;
        })
      } else {
        console.log("实时");
        this.getListRealtime()
      }
    },

    initWebSocket(){ //初始化weosocket
      const wsuri = "ws://60.204.149.135:8080/ws/socketServer/1/homework"
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onopen = this.websocketonopen;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    websocketonopen(){ //连接建立之后执行send方法发送数据
      console.log('连接建立之后执行send方法发送数据');
    },
    websocketonerror(){//连接建立失败重连
      console.log('连接建立失败重连');
      this.$message.error("连接建立失败重连")
      this.initWebSocket();
    },
    websocketonmessage(e){ //数据接收
      let msg = JSON.parse(JSON.parse(e.data).message)
      console.log('数据接收',msg);
      if(msg.type == "error") {
        this.$notify({
          title: '警告',
          message: msg.content,
          type: 'error'
        });
      } else if(msg.type == "warning") {
        this.$notify({
          title: '警告',
          message: msg.content,
          type: 'warning'
        });
      } else {
        this.datas = {...msg}
      }
      
    },
    websocketclose(e){  //关闭
      console.log('断开连接',e);
      // this.$message.error("断开连接")
    }

  }
};
</script>
<style scoped>
.input-width {
  width: 203px;
}
.app-container .el-dialog {
  width: 70% !important;
  margin-top: 20px !important;
}
.app-container .el-dialog__body {
  height: 550px;
  width: 100%;
  overflow: auto;
}
.app-container img {
  max-width: 100%;
}

.search .el-card__body {
  padding: 0;
  padding-right: 20px;
}
.export-excel-wrapper {
  float: right;
}
.el-btn {
  margin-top:20px !important;
}
</style>
