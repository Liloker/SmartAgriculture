import request from '@/utils/request'

export function upload(data) {
  return request({
    url: 'http://60.204.149.135/api/upload/rec',
    method: 'post',
    data: data
  })
}