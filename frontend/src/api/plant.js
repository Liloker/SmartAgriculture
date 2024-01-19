import request from '@/utils/request'

export function fetchPlantList(params) {
  return request({
    url: 'http://60.204.149.135/api/farmproduct/list',
    method: 'get',
    params: params
  })
}

export function deletePlant(data) {
  return request({
    url: 'http://60.204.149.135/api/farmproduct/delete',
    method: 'post',
    data: data
  })
}

export function createPlant(data) {
  return request({
    url: 'http://60.204.149.135/api/farmproduct/insert',
    method: 'post',
    data: data
  })
}

export function updatePlant(data) {
  return request({
    url: 'http://60.204.149.135/api/farmproduct/update',
    method: 'post',
    data: data
  })
}