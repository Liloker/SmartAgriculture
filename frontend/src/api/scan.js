import request from '@/utils/request'

export function scanLog(params) {
  return request({
    url: 'http://60.204.149.135/api/upload/list',
    method: 'get',
    params: params
  })
}


export function deleteLog(data) {
  return request({
    url: 'http://60.204.149.135/api/upload/delete',
    method: 'post',
    data: data
  })
}