<template>
  <div class="app-container app-container-wx">
    <div class="search">
      <el-card class="filter-container" shadow="never">
        <div style="margin-top: 15px">
          <el-form
            :inline="true"
            :model="listQuery"
            size="small"
            label-width="140px"
          >
            <el-form-item label="请输入">
              <el-input
                v-model="listQuery.mobile"
                class="input-width"
                placeholder="手机号"
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
        <el-table-column label="手机号" width="150" align="center">
          <template slot-scope="scope">{{ scope.row.mobile }}</template>
        </el-table-column>
        <el-table-column label="注册时间" width="200" align="center">
          <template slot-scope="scope">{{ scope.row.createTime }}</template>
        </el-table-column>
        <el-table-column label="客户状态" align="center">
          <template slot-scope="scope">{{ scope.row.stateDescription }}</template>
        </el-table-column>
        <el-table-column label="银行开户状态" align="center">
          <template slot-scope="scope">{{ scope.row.bankState == 1 ? '已开通' : '未开通' }}</template>
        </el-table-column>
        <el-table-column label="下单时间" align="center">
          <template slot-scope="scope">{{ scope.row.orderTime }}</template>
        </el-table-column>
        <el-table-column label="金额" align="center">
          <template slot-scope="scope">{{ scope.row.orderAmount }}</template>
        </el-table-column>
        <el-table-column label="购买份数" align="center">
          <template slot-scope="scope">{{ scope.row.orderQuantity }}</template>
        </el-table-column>
        <el-table-column label="备注" align="center">
          <template slot-scope="scope">{{ scope.row.remark }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200"  align="center">
          <template slot-scope="scope">
           <span @click="addRemark(scope.row)" class="link">备注</span>
           <a :href="scope.row.accountBalanceTableUrl" v-if="scope.row.accountBalanceTableUrl" class="link" style="margin-left: 10px">下期初</a>
           <span @click="deleteConfirm(scope.row)" class="link">删除</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="pagination-container">
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        layout="total, sizes,prev, pager, next,jumper"
        :current-page.sync="listQuery.pageNum"
        :page-size="listQuery.pageSize"
        :page-sizes="[25, 50, 100]"
        :total="total"
      ></el-pagination>
    </div>

    <div class="zhizhao">
      <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
        <el-form
          label-width="100px"
          size="small"
          :model="ruleForm"
          ref="ruleForm"
        >
          <el-form-item label="标题：" prop="title">
            <el-input 
            type="textarea"
            class="remark"
            v-model="ruleForm.remark"></el-input>
          </el-form-item>
          <el-form-item class="el-btn">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="submit">确 定</el-button>
          </el-form-item>

        </el-form>
      </el-dialog>
    </div>

  </div>
</template>
<script>
import {
  deleteMember,
  fetchList,
  saveRemark
} from "@/api/member";
const defaultListQuery = {
  current: 1,
  size: 25,
  mobile: "",
};
export default {
  name: "orderList",
  data() {
    return {
      listQuery: Object.assign({}, defaultListQuery),
      listLoading: true,
      list: null,
      total: null,
      dialogVisible: false,
      ruleForm: {
        id: null,
        remark: ""
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    submit() {
      saveRemark(this.ruleForm).then(res => {
        this.dialogVisible = false
        this.getList();
      })
    },  
    addRemark(row) {
      this.dialogVisible = true
      this.ruleForm = {...row}
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
    handleSizeChange(val) {
      this.listQuery.pageNum = 1;
      this.listQuery.pageSize = val;
      this.getList();
    },
    handleCurrentChange(val) {
      this.listQuery.pageNum = val;
      this.getList();
    },
    getList() {
      this.listLoading = true;
      fetchList(this.listQuery).then(response => {
        this.listLoading = false;
        this.list = response.data.records;
        this.total = response.data.total;
      });
    },
    deleteConfirm(val) {
      this.$confirm('危险操作，确定删除吗', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '确定',
          cancelButtonText: '放弃'
        })
          .then(() => {
            deleteMember({id: val.id}).then(res => {
              this.getList();
            })
          })
          .catch(action => {

          })
    }
  }
};
</script>
<style scoped>
.input-width {
  width: 203px;
}
</style>

<style>
.zhizhao .el-dialog {
  width: 70% !important;
  margin-top: 20px !important;
}
.zhizhao .el-dialog__body {
  height: 450px;
  width: 100%;
  overflow: auto;
}
.zhizhao img {
  max-width: 100%;
}

.remark .el-textarea__inner{
  height: 200px;
}
</style>
