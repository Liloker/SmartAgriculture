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
            <el-form-item label="按位置筛选：">
              <el-select placeholder="请选择">
                <el-option key="位置1" label="位置1" value="位置1"></el-option>
                <el-option key="位置2" label="位置2" value="位置2"></el-option>
                <el-option key="位置3" label="位置3" value="位置3"></el-option>
                <el-option key="位置4" label="位置4" value="位置4"></el-option>
              </el-select>
            </el-form-item>

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
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span>
      <el-button type="primary" class="btn-add" size="mini" @click="handleAdd">新增传感器</el-button>
    </el-card>
    <div class="table-container">
      <el-table
        ref="orderTable"
        :data="list"
        style="width: 100%;"
        @selection-change="handleSelectionChange"
        v-loading="listLoading"
        border
      >
        <el-table-column label="传感器编号" width="400" align="left">
          <template slot-scope="scope">{{ scope.row.id }}</template>
        </el-table-column>
        <el-table-column label="传感器名称" align="left">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="传感器位置" align="left">
          <template slot-scope="scope">{{ scope.row.position }}</template>
        </el-table-column>
        <el-table-column label="传感器类型" align="left">
          <template slot-scope="scope">{{ scope.row.sensor_type }}</template>
        </el-table-column>
        <el-table-column label="所在大棚" align="left">
          <template slot-scope="scope">{{ scope.row.greenhouse_name }}</template>
        </el-table-column>

        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>


  <el-dialog
    title="新增传感器"
    :visible.sync="dialogAddVisible"
    width="500px">
    
    <el-form
      label-width="100px"
      size="small"
      :model="ruleForm"
      ref="ruleForm"
    >
      <el-form-item label="传感器名称：" prop="title">
        <el-input v-model="ruleForm.name"></el-input>
      </el-form-item>
      <el-form-item label="传感器类型：" prop="title">
        <el-select v-model="ruleForm.sensor_type" placeholder="请选择">
          <el-option 
            v-for="item in types"
            :key="item"
            :label="item"
            :value="item"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="传感器位置：" prop="title">
        <el-input v-model="ruleForm.position"></el-input>
      </el-form-item>
      <el-form-item label="所属大棚：" prop="title">
        <el-select placeholder="请选择" v-model="ruleForm.greenhouse_id">
          <el-option 
            v-for="item in greenhouses"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="报警阈值：" prop="title">
        <el-input v-model="ruleForm.alert_threshold"></el-input>
      </el-form-item>

      <el-form-item class="el-btn">
        <el-button @click="dialogAddVisible = false">取 消</el-button>
        <el-button type="primary" @click="submit">确 定</el-button>
      </el-form-item>

    </el-form>
  </el-dialog>

  </div>
</template>
<script>
import { fetchSensorList, createSensor, deleteSensor, updateSensor, fetchTypeList} from "@/api/sensor";
import { fetchGreenhouseList } from "@/api/greenhouse";

const defaultListQuery = {
  keyword: ''
};
export default {
  name: "orderList",
  data() {
    return {
      listQuery: Object.assign({}, defaultListQuery),
      listLoading: false,
      list: [],
      greenhouses: [],
      types: [],
      total: null,
      dialogAddVisible: false,
      ruleForm: {
        id: null,
        title: "",
        content: ""
      }
    };
  },
  created() {
    this.getList();
    fetchGreenhouseList().then(res => {
      this.greenhouses = res.data;
    })
    fetchTypeList().then(res => {
      this.types = res.data;
    })
  },
  methods: {
    handleAdd() {
      this.ruleForm = {}
      this.dialogAddVisible = true;
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
        
        deleteSensor({id: id}).then(res => {
          this.getList();
        })
      });
    },  
    handleEdit(row) {
      this.ruleForm = {...row}
      this.dialogAddVisible = true
    },
    handleResetSearch() {
      this.listQuery = Object.assign({}, defaultListQuery);
    },
    handleSearchList() {
      this.getList();
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    getList() {
      this.listLoading = true;
      fetchSensorList(this.listQuery).then(response => {
        this.listLoading = false;
        this.list = response.data;
      });
    },
    submit() {
      if (this.ruleForm.id) {
        updateSensor(this.ruleForm).then(res => {
          this.dialogAddVisible = false
          this.getList();
        })
      } else {
        createSensor(this.ruleForm).then(res => {
          this.dialogAddVisible = false
          this.getList();
        })
      }
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
