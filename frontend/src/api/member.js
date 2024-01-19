import request from '@/utils/request'
export function fetchList(params) {
  return request({
    url: '/admin/member/list',
    method: 'get',
    params: params
  })
}

export function saveRemark(data) {
  return request({
    url: '/admin/member/saveRemark',
    method: 'post',
    data: data
  })
}

export function deleteMember(params) {
  return request({
    url: '/admin/member/deleteMember',
    method: 'get',
    params: params
  })
}
