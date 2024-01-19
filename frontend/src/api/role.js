import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/admin/role',
    method: 'get',
    params: params
  })
}

export function fetchAll() {
  return request({
    url: '/admin/role/all/index',
    method: 'get',
  })
}

export function detail(params) {
  return request({
    url: '/admin/role/' + params,
    method: 'get'
  })
}

export function addRole(params) {
  return request({
    url: '/admin/role',
    method: 'post',
    data: params
  })
}

export function deleteRole(params) {
  return request({
    url: '/admin/role/' + params,
    method: 'delete',
  })
}

export function updateRole(id, params) {
  return request({
    url: '/admin/role/' + id,
    method: 'put',
    data: params
  })
}