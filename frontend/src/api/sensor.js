import request from '@/utils/request'

export function fetchSensorList(params) {
  return request({
    url: 'http://60.204.149.135/api/sensor/list',
    method: 'get',
    params: params
  })
}

export function deleteSensor(data) {
  return request({
    url: 'http://60.204.149.135/api/sensor/delete',
    method: 'post',
    data: data
  })
}

export function createSensor(data) {
  return request({
    url: 'http://60.204.149.135/api/sensor/insert',
    method: 'post',
    data: data
  })
}

export function updateSensor(data) {
  return request({
    url: 'http://60.204.149.135/api/sensor/update',
    method: 'post',
    data: data
  })
}

export function fetchTypeList(params) {
  return request({
    url: 'http://60.204.149.135/api/sensor/listtype',
    method: 'get',
    params: params
  })
}
