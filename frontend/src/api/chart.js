import request from '@/utils/request'

export function getChartList(data) {
  return request({
    url: 'http://60.204.149.135/api/sensordata/history',
    method: 'post',
    data: data
  })
}

export function getChartListRealtime(data) {
  return request({
    url: 'http://60.204.149.135/api/sensordata/realtime',
    method: 'post',
    data: data
  })
}

export function stopChartListRealtime(data) {
  return request({
    url: 'http://60.204.149.135/api/sensordata/stop',
    method: 'post',
    data: data
  })
}