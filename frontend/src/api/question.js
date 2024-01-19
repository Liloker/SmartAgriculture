import request from '@/utils/request'

export function fetchQuestionList(params) {
  return request({
    url: 'http://60.204.149.135/api',
    method: 'get',
    params: params
  })
}