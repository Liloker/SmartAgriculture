<template>
  <el-card class="form-container" shadow="never">
    <el-form
      :model="adminForm"
      :rules="rules"
      ref="adminForm"
      label-width="150px"
      size="small"
    >
      <el-form-item label="用户名：" prop="username">
        <el-input v-model="adminForm.username" class="input-width"></el-input>
      </el-form-item>
      <el-form-item label="密码：" prop="password">
        <el-input
          type="password"
          v-model="adminForm.password"
          class="input-width"
        ></el-input>
      </el-form-item>
      <el-form-item label="确认密码：" prop="password">
        <el-input
          type="password"
          v-model="adminForm.passwordConfirm"
          class="input-width"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit('adminForm')"
          >提交</el-button
        >
        <el-button v-if="!isEdit" @click="resetForm('adminForm')"
          >重置</el-button
        >
      </el-form-item>
    </el-form>
  </el-card>
</template>
<script>
import { createAdmin, getAdmin, updateAdmin } from "@/api/admin";

export default {
  name: "AdminDetail",
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      adminForm: {
        username: "",
        password: "",
        companyId: "",
        passwordConfirm: "",
        auth: ["1", "2"]
      },
      companys:[],
      roles:[],
      rules: {
        username: [
          { required: true, message: "请输入名称", trigger: "blur" },
          {
            min: 2,
            max: 140,
            message: "长度在 2 到 140 个字符",
            trigger: "blur"
          }
        ]
      }
    };
  },
  created() {
    if (this.isEdit) {
      getAdmin(this.$route.query.id).then(response => {
        this.adminForm = response.data;
      });
    }
  },
  methods: {
    onSubmit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$confirm("是否提交数据", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }).then(() => {
            if (this.isEdit) {
              updateAdmin(this.$route.query.id, this.adminForm).then(
                response => {
                  this.$refs[formName].resetFields();
                  this.$message({
                    message: "修改成功",
                    type: "success",
                    duration: 1000
                  });
                  this.$router.back();
                }
              );
            } else {
              createAdmin(this.adminForm).then(response => {
                this.$refs[formName].resetFields();
                this.$message({
                  message: "提交成功",
                  type: "success",
                  duration: 1000
                });
                this.$router.back();
              });
            }
          });
        } else {
          this.$message({
            message: "验证失败",
            type: "error",
            duration: 1000
          });
          return false;
        }
      });
    }
  }
};
</script>
<style scoped>
.input-width {
  width: 60%;
}
</style>
