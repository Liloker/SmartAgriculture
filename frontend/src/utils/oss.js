'use strict'
import {
    dateFormat
} from '@/utils/util'

var OSS = require('ali-oss')

export default {

    /**
     * 创建随机字符串
     * @param num
     * @returns {string}
     */
    randomString(num) {
        const chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        let res = ''
        for (let i = 0; i < num; i++) {
            var id = Math.ceil(Math.random() * 35)
            res += chars[id]
        }
        return res
    },

    /**
     * 创建oss客户端对象
     * @returns {*}
     */
    createOssClient() {
        return new Promise((resolve, reject) => {
            const client = new OSS({
                region: 'oss-cn-hangzhou', // 请设置成你的
                accessKeyId: 'LTAI9TQaIzYtTNKd', // 请设置成你的
                accessKeySecret: 'xqt7FyIAfVYh7Zs0903o3G7SsdtxWS', // 请设置成你的
                bucket: 'sh-check' // 请设置成你的
            })
            resolve(client)
        })
    },
    /**
     * 文件上传
     * @param option 参考csdn: https://blog.csdn.net/qq_27626333/article/details/81463139
     */
    ossUploadFile(option) {
        const file = option.file
        const self = this
        return new Promise((resolve, reject) => {
            const date = dateFormat(new Date(), 'yyyyMMdd') // 当前时间
            const dateTime = dateFormat(new Date(), 'yyyyMMddhhmmss') // 当前时间
            const randomStr = self.randomString(4) //  4位随机字符串
            const extensionName = file.name.substr(file.name.indexOf('.')) // 文件扩展名
            const fileName = 'video/' + date + '/' + dateTime + '_' + randomStr + extensionName // 文件名字（相对于根目录的路径 + 文件名）
            // 执行上传
            self.createOssClient().then(client => {
                // 异步上传,返回数据
                resolve({
                    fileName: file.name,
                    fileUrl: fileName
                })
                // 上传处理
                // 分片上传文件
                client.multipartUpload(fileName, file, {
                    progress: function (p) {
                        const e = {}
                        e.percent = Math.floor(p * 100)
                        // console.log('Progress: ' + p)
                        option.onProgress(e)
                    }
                }).then((val) => {
                    console.info(val)
                    if (val.res.statusCode === 200) {
                        option.onSuccess(val)
                        return val
                    } else {
                        option.onError('上传失败')
                    }
                }, err => {
                    option.onError('上传失败')
                    reject(err)
                })
            })
        })
    }
}