<template>
  <div class="app-container">
    <el-tabs type="border-card" v-model="activeName">
      <el-tab-pane label="识别" name="first">
        <div class="upload-div">
          <el-upload
            class="upload-demo"
            drag
            action="http://60.204.149.135/api/upload/rec"
            :on-success="handleSuccess"
            name="image"
            :data="formData"
            multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </el-upload>
        </div>
      </el-tab-pane>
      <el-tab-pane label="识别历史" name="second">
        
        <div class="table-container">
          <el-table
            ref="orderTable"
            :data="list"
            style="width: 100%;"
            v-loading="listLoading"
            border
          >
            <el-table-column label="图片文件名" width="400" align="left">
              <template slot-scope="scope">{{ scope.row.image_name }}</template>
            </el-table-column>
            <el-table-column label="识别结果" align="left">
              <template slot-scope="scope">有{{ scope.row.pest_num }}只虫</template>
            </el-table-column>
            <el-table-column label="识别时间" align="left">
              <template slot-scope="scope">{{ scope.row.rec_date }}</template>
            </el-table-column>
            <el-table-column label="大棚名称" align="left">
              <template slot-scope="scope">{{ scope.row.greenhouse_name }}</template>
            </el-table-column>

            <el-table-column label="操作" width="250" align="center">
              <template slot-scope="scope">
                <el-button type="primary" size="mini" @click="handleDetail(scope.row)">浏览</el-button>
                <el-button type="danger" size="mini" @click="handleDelete(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="30%">
      
      <el-image 
        style="width: 100%;"
        :src="url">
      </el-image>

    </el-dialog>
  </div>
</template>
<script>
import { scanLog, deleteLog } from "@/api/scan";

export default {
  name: "orderList",
  data() {
    return {
      activeName: 'second',
      list: [],
      dialogVisible: false,
      listLoading: false,
      url: "",
      formData : {
        greenhouse_id: 1
      }
    };
  },
  created() {
    this.getList()
  },
  methods: {

    getList() {
      scanLog().then(res => {
        this.list = res.data
      })
    },

    handleDetail(row) {
      this.url = "http://60.204.149.135/images/" + row.image_name
      this.dialogVisible = true
    },

    handleDetailClose() {
      this.dialogVisible = false
    },

    handleSuccess() {
      scanLog().then(res => {
        this.list = res.data
        this.activeName = "second"
      })
    },

    handleDelete(id) {
      this.$confirm(
        "确定删除吗？",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        deleteLog({id}).then(res => {
          this.getList();
        })
      });
    },  
  }
};
</script>

<style scoped>
.upload-div {
  text-align: center;
  margin-top: 100px;
  min-height: 400px;
}
</style>