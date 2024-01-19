import request from '@/utils/request'

export function fetchProductionCycleList(data) {
  return request({
    url: 'http://60.204.149.135/api/productcycle/list',
    method: 'post',
    data: data
  })
}

export function deleteProductionCycle(data) {
  return request({
    url: 'http://60.204.149.135/api/productcycle/delete',
    method: 'post',
    data: data
  })
}

export function createProductionCycle(data) {
  return request({
    url: 'http://60.204.149.135/api/productcycle/insert',
    method: 'post',
    data: data
  })
}

export function updateProductionCycle(data) {
  return request({
    url: 'http://60.204.149.135/api/productcycle/update',
    method: 'post',
    data: data
  })
}