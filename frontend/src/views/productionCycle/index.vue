<template>
  <div class="app-container">
    <el-card class="operate-container" shadow="never">
      <span>农产品名称：{{name}}</span>
      <span style="margin-left: 100px;">所在大棚：{{ruleForm.farmproduct_id}}</span>
      <el-button type="primary" class="btn-add" size="mini" @click="handleAdd">新增周期</el-button>
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
        <el-table-column label="周期编号" width="400" align="left">
          <template slot-scope="scope">{{ scope.row.id }}</template>
        </el-table-column>
        <el-table-column label="农产品周期" align="left">
          <template slot-scope="scope">{{ scope.row.cycle_name }}</template>
        </el-table-column>
        <el-table-column label="最近时间点" align="left">
          <template slot-scope="scope">{{ scope.row.date }}</template>
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
    title="新增生产周期"
    :visible.sync="dialogAddVisible"
    width="500px">
    
    <el-form
      label-width="100px"
      size="small"
      :model="ruleForm"
      ref="ruleForm"
    >
      <el-form-item label="农产品周期：" prop="title">
        <el-input v-model="ruleForm.cycle_name"></el-input>
      </el-form-item>
      <el-form-item label="时间点：" prop="title">
        <el-date-picker
          v-model="ruleForm.date"
          type="date"
          placeholder="选择日期"
          value-format="yyyy-MM-dd"
          >
        </el-date-picker>
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
import { fetchProductionCycleList, createProductionCycle, deleteProductionCycle, updateProductionCycle} from "@/api/productionCycle";

export default {
  name: "orderList",
  data() {
    return {
      listLoading: false,
      list: [],
      greenhouses: [],
      types: [],
      name: this.$route.query.name,
      greenhouse_name: this.$route.query.greenhouse_name,
      dialogAddVisible: false,
      ruleForm: {
        farmproduct_id : 123,
        cycle_name: "",
        date: null
      }
    };
  },
  created() {
    this.ruleForm.farmproduct_id = this.$route.query.farmproduct_id;
    console.log("111", this.ruleForm);
    this.getList();
  },
  methods: {
    handleAdd() {
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
        
        deleteProductionCycle({productcycle_id: id}).then(res => {
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
      fetchProductionCycleList({farmproduct_id : this.$route.query.farmproduct_id}).then(response => {
        this.listLoading = false;
        this.list = response.data;
      });
    },
    submit() {
      console.log("ruleForm", this.ruleForm);
      if (this.ruleForm.id) {
        updateProductionCycle(this.ruleForm).then(res => {
          this.dialogAddVisible = false
          this.getList();
        })
      } else {
        createProductionCycle(this.ruleForm).then(res => {
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
