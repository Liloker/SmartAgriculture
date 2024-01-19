import request from '@/utils/request'

export function fetchGreenhouseList(params) {
  return request({
    url: 'http://60.204.149.135/api/greenhouse/list',
    method: 'get',
    params: params
  })
}

export function deleteGreenhouse(data) {
  return request({
    url: 'http://60.204.149.135/api/greenhouse/delete',
    method: 'post',
    data: data
  })
}

export function createGreenhouse(data) {
  return request({
    url: 'http://60.204.149.135/api/greenhouse/insert',
    method: 'post',
    data: data
  })
}

export function updateGreenhouse(data) {
  return request({
    url: 'http://60.204.149.135/api/greenhouse/update',
    method: 'post',
    data: data
  })
}