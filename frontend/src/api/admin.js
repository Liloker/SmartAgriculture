import request from '@/utils/request'
export function fetchList(params) {
  return request({
    url: '/admin/list',
    method: 'get',
    params: params
  })
}

export function deleteAdmin(params) {
  return request({
    url: '/admin/delete',
    method: 'delete',
    params: params
  })
}

export function createAdmin(data) {
  return request({
    url: '/admin/create',
    method: 'post',
    data: data
  })
}

export function getAdmin(id) {
  return request({
    url: '/admin/' + id,
    method: 'get',
  })
}

export function updateAdmin(id, data) {
  return request({
    url: '/admin/' + id,
    method: 'put',
    data: data
  })
}