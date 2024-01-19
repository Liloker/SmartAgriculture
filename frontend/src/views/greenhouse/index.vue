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
            <el-form-item label="输入搜索：">
              <el-input
                v-model="listQuery.keyword"
                class="input-width"
                placeholder="名称"
              ></el-input>
            </el-form-item>

            <el-form-item style="margin-left:50px;">
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
      <el-button type="primary" class="btn-add" size="mini" @click="handleAdd">新增大棚</el-button>
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
        <el-table-column label="大棚编号" width="400" align="left">
          <template slot-scope="scope">{{ scope.row.id }}</template>
        </el-table-column>
        <el-table-column label="大棚名称" align="left">
          <template slot-scope="scope">{{ scope.row.name }}</template>
        </el-table-column>
        <el-table-column label="传感器数量" align="left">
          <template slot-scope="scope">{{ scope.row.count }}</template>
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
    title="新增大棚"
    :visible.sync="dialogAddVisible"
    width="500px">
    
    <el-form
      label-width="100px"
      size="small"
      :model="ruleForm"
      ref="ruleForm"
    >
      <el-form-item label="大棚名称：" prop="title">
        <el-input v-model="ruleForm.name"></el-input>
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
import { fetchGreenhouseList, createGreenhouse, updateGreenhouse, deleteGreenhouse} from "@/api/greenhouse";

const defaultListQuery = {
  current: 1,
  size: 25,
  keyword: ''
};
export default {
  name: "orderList",
  data() {
    return {
      listQuery: Object.assign({}, defaultListQuery),
      listLoading: false,
      list: [],
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
        
        deleteGreenhouse({id}).then(res => {
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
      this.listQuery.pageNum = 1;
      this.getList();
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    getList() {
      this.listLoading = true;
      fetchGreenhouseList(this.listQuery).then(response => {
        this.listLoading = false;
        this.list = response.data;
      });
    },
    submit() {
      if (this.ruleForm.id) {
        updateGreenhouse(this.ruleForm).then(res => {
          this.dialogAddVisible = false
          this.getList();
        })
      } else {
        createGreenhouse(this.ruleForm).then(res => {
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
