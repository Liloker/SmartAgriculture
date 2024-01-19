<template>
  <div>
    <el-upload
      action="http://sh-check.oss-cn-hangzhou.aliyuncs.com"
      :data="dataObj"
      :multiple="false"
      :show-file-list="showFileList"
      :file-list="fileList"
      :on-success="handleUploadSuccess"
      :before-upload="beforeAvatarUpload"
      :on-progress="handleProgress"
    >
      <el-button size="small" type="primary">点击上传</el-button>
      <div slot="tip" class="el-upload__tip">格式支持MP4，大小不超过2G，建议视频分辨率为1280×720</div>
    </el-upload>
    <el-progress :percentage="percentage"></el-progress>
  </div>
</template>
<script>
import { policy, createName } from "@/api/oss";
export default {
  name: "singleUpload",
  data() {
    return {
      dataObj: {
        policy: "",
        signature: "",
        key: "",
        ossaccessKeyId: "",
        dir: "",
        host: ""
      },
      videoUrl: "",
      videoDuration: null,
      actionUrl: process.env.BASE_API + "/attachment",
      percentage: 0
    };
  },
  computed: {
    fileList() {
      return [
        {
          name: this.videoUrl,
          url: this.videoUrl
        }
      ];
    },
    showFileList: {
      get: function() {
        return this.videoUrl !== "";
      },
      set: function(newValue) {}
    }
  },
  methods: {
    handleUploadSuccess(res, file) {
      console.log("成功");
      this.videoUrl = res.data;
      this.showFileList = true;
      this.fileList.pop();
      this.fileList.push({
        name: res.data,
        url: res.data
      });
    },
    createName(file) {
      let fileName = file.name;
      let ext = fileName.split(".")[fileName.split(".").length - 1];

      var now = new Date();
      var year = now.getFullYear() + ""; //得到年份
      var month = now.getMonth() + ""; //得到月份
      var date = now.getDate() + ""; //得到日期
      var hour = now.getHours() + ""; //得到小时
      var minu = now.getMinutes() + ""; //得到分钟
      month = month + 1;
      if (month < 10) month = "0" + month;
      if (date < 10) date = "0" + date;
      var number = now.getSeconds() % 43; //这将产生一个基于目前时间的0到42的整数。
      var time = year + month + date + hour + minu;
      return time + "_" + number + "." + ext;
    },
    beforeAvatarUpload(file) {
      var fileName = file.name;
      var ext = fileName.split(".")[fileName.split(".").length - 1];
      // 获取视频时长
      var url = URL.createObjectURL(file);
      var audioElement = new Audio(url);
      var duration;

      let newName = this.createName(file);
      this.videoUrl = newName;

      let _this = this;
      audioElement.addEventListener("loadedmetadata", function(_event) {
        duration = audioElement.duration; //时长为秒，小数，182.36
        console.log(duration);
        _this.videoDuration = _this.secondsFormat(parseInt(duration));

        _this.$emit("setVideo", {
          videoUrl:
            "http://sh-check.oss-cn-hangzhou.aliyuncs.com/video/" +
            _this.videoUrl,
          videoDuration: _this.videoDuration
        });
      });

      let _self = this;
      return new Promise((resolve, reject) => {
        policy()
          .then(response => {
            _self.dataObj.policy = response.data.policy;
            _self.dataObj.signature = response.data.signature;
            _self.dataObj.ossaccessKeyId = response.data.accessId;
            _self.dataObj.key = response.data.dir + "/" + newName;
            _self.dataObj.dir = response.data.dir;
            _self.dataObj.host = response.data.host;
            resolve(true);
          })
          .catch(err => {
            console.log(err);
            reject(false);
          });
      });
    },
    secondsFormat(s) {
      var minute = Math.floor(s / 60);
      var second = s - minute * 60;

      minute = "00" + minute;
      second = "00" + second;
      return minute.slice(-2) + ":" + second.slice(-2);
    },
    handleProgress(progressEvent, file, fileList) {
      let percent = ((progressEvent.loaded / progressEvent.total) * 100) | 0;
      this.percentage = percent;
    }
  }
};
</script>
<style></style>
