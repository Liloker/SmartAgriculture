<template>
  <div>
    <div>
      <el-upload
        class="avatar-uploader"
        :action="actionUrl"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </div>
    <div class="remark">
      <slot></slot>
    </div>
  </div>
</template>
<script>
import { policy } from "@/api/oss";

export default {
  data() {
    return {
      imageUrl: "",
      actionUrl: process.env.BASE_API + "/attachment"
    };
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw);
      this.$emit("setImg", res.data);
      this.$emit("stopLoading");
    },
    beforeAvatarUpload(file) {
      this.$emit("loading");
      // const isJPG = file.type === "image/jpeg";
      const isLt2M = file.size / 1024 / 1024 < 2;

      // if (!isJPG) {
      //   this.$message.error("上传头像图片只能是 JPG 格式!");
      // }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }
      return isLt2M;
    }
  }
};
</script>
<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  float: left;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
.remark {
  font-size: 14px;
  float: left;
  margin-left: 10px;
  width: 500px;
  line-height: 2.2em;
  color: #8c939d;
}
</style>


