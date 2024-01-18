from flask import request, jsonify
from flask_models import *
from smutils import *
import threading
import time
# from websocket import create_connection
import json
import http.client
import urllib.parse

# 连接地址是：ws://60.204.149.135/ws/socketServer/1/homework
# 其中1是userId可以随便写，homework是groupid

CURRENT_GREENHOUSE_ID = None

# ws_url = "ws://127.0.0.1:5431/api/sensordata"
ws_url = "http://60.204.149.135/ws/sendAll"
ws_host = "60.204.149.135"


# return_msg = {
#         "chat1":{
#             "columns": ['日期', '空气温度'],
#             "rows": [
#                 { '日期': '1/1', '空气温度': 1393 },
#                 { '日期': '1/2', '空气温度': 3530 },
#                 { '日期': '1/3', '空气温度': 2923 },
#                 { '日期': '1/4', '空气温度': 1723 },
#                 { '日期': '1/5', '空气温度': 3792 },
#                 { '日期': '1/6', '空气温度': 4593 }
#             ]
#         },

#         "chat2" : {
#             "columns": ['日期', '空气湿度'],
#             "rows": [
#                 { '日期': '1/1', '空气湿度': 1393 },
#                 { '日期': '1/2', '空气湿度': 3530 },
#                 { '日期': '1/3', '空气湿度': 2923 },
#                 { '日期': '1/4', '空气湿度': 1723 },
#                 { '日期': '1/5', '空气湿度': 3792 },
#                 { '日期': '1/6', '空气湿度': 4593 }
#             ]
#         },
#         "chat3" : {
#             "columns": ['日期', '二氧化碳浓度'],
#             "rows": [
#                 { '日期': '1/1', '二氧化碳浓度': 1393 },
#                 { '日期': '1/2', '二氧化碳浓度': 3530 },
#                 { '日期': '1/3', '二氧化碳浓度': 2923 },
#                 { '日期': '1/4', '二氧化碳浓度': 1723 },
#                 { '日期': '1/5', '二氧化碳浓度': 3792 },
#                 { '日期': '1/6', '二氧化碳浓度': 4593 }
#             ]
#         },
#         "chat4" : {
#             "columns": ['日期', '光照度'],
#             "rows": [
#                 { '日期': '1/1', '光照度': 1393 },
#                 { '日期': '1/2', '光照度': 3530 },
#                 { '日期': '1/3', '光照度': 2923 },
#                 { '日期': '1/4', '光照度': 1723 },
#                 { '日期': '1/5', '光照度': 3792 },
#                 { '日期': '1/6', '光照度': 4593 }
#             ]
#         },
#         "chat5" : {
#             "columns": ['日期', '土壤温度'],
#             "rows": [
#                 { '日期': '1/1', '土壤温度': 1393 },
#                 { '日期': '1/2', '土壤温度': 3530 },
#                 { '日期': '1/3', '土壤温度': 2923 },
#                 { '日期': '1/4', '土壤温度': 1723 },
#                 { '日期': '1/5', '土壤温度': 3792 },
#                 { '日期': '1/6', '土壤温度': 4593 }
#             ]
#         },
#         "chat6" : {
#             "columns": ['日期', '土壤湿度'],
#             "rows": [
#                 { '日期': '1/1', '土壤湿度': 1393 },
#                 { '日期': '1/2', '土壤湿度': 3530 },
#                 { '日期': '1/3', '土壤湿度': 2923 },
#                 { '日期': '1/4', '土壤湿度': 1723 },
#                 { '日期': '1/5', '土壤湿度': 3792 },
#                 { '日期': '1/6', '土壤湿度': 4593 }
#             ]
#         }
#     }

def gen_data(greenhouse_id):
    n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    x = random_generate_data()

    sd = SensorData(greenhouse_id=greenhouse_id,
                    carbon_dioxide=x['carbon_dioxide'],
                    air_temperature=x['air_temperature'],
                    air_moisture=x['air_moisture'],
                    light_intensity=x['light_intensity'],
                    soil_temperature=x['soil_temperature'],
                    soil_moisture=x['soil_moisture']
                    )

    db.session.add(sd)
    db.session.commit()

    real = db.session.query(SensorData).filter(
        SensorData.greenhouse_id == greenhouse_id).order_by(SensorData.dt.desc()).limit(20)
    

    sortl = sorted(real, key=lambda r: r.dt)
    l = [x.to_dict() for x in sortl]
    # d = {"sensor_data": x, "ts": n, "greenhouse_id": greenhouse_id}
    return l


# @app.before_first_request
def activate_job():
    def run_job():
        with app.test_request_context():
            global CURRENT_GREENHOUSE_ID
            # ws = create_connection(ws_url)
            ws = http.client.HTTPConnection(ws_host, timeout=10)
            headers = {"Content-Type": "application/json"}
            # print("获取ws连接状态 : ", ws.connected)
            while True:

                sleep_time = random.randrange(1, 10, 1)
                if CURRENT_GREENHOUSE_ID == None:
                    time.sleep(1)
                    continue
                print("执行后台发送传感器数据任务...")
                print("当前大棚id : {}".format(CURRENT_GREENHOUSE_ID))

                d = gen_data(CURRENT_GREENHOUSE_ID)
                return_msg = convert_orm_to_showing_sensor_data(d)
                try:
                    # params = {
                    #     "group": "homework",
                    #     "msg": return_msg
                    # }
                    params = {
                        "fromUserId": "homework",
                        "msg": "\{\"test\"\}",
                        "userIds": [1]
                    }

                    # p = urllib.parse.urlencode(params)
                    # ws.send(json.dumps(d))
                    # ws.request("GET", "/ws/sendAll?" + p, p, headers)
                    # param_json = json.dumps(params)
                    # param_json = json.dumps(params, ensure_ascii=False).decode(
                    #     'utf8').encode('gb2312')

                    params["msg"] = json.dumps(return_msg)

                    param_json = json.dumps(params, ensure_ascii=False)
                    print(param_json)
                    ws.request("POST", "/ws/sendMessage",
                               param_json, headers)

                    r1 = ws.getresponse()
                    # This will return entire content.
                    data = r1.read().decode('utf8')
                    print(data)
                except Exception as e:
                    print(e)
                    ws = http.client.HTTPConnection(ws_host, timeout=10)

                time.sleep(sleep_time)

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/api/sensordata/history', methods=['POST'])
def history_sensordata():
    greenhouse_id = request.json['greenhouse_id']
    sd = request.json['start_date']
    ed = request.json['end_date']

    result = success_result.copy()
    history = get_history_sensordata(greenhouse_id, sd, ed)
    ret_data = convert_orm_to_showing_sensor_data(history)
    result["data"] = ret_data
    return jsonify(result)


@app.route('/api/sensordata/realtime', methods=['POST'])
def realtime_sensordata():
    greenhouse_id = request.json['greenhouse_id']

    global CURRENT_GREENHOUSE_ID
    CURRENT_GREENHOUSE_ID = greenhouse_id
    result = success_result.copy()
    result["msg"] = "开始发送实时传感器数据"
    return jsonify(result)


@app.route('/api/sensordata/error', methods=['GET','POST'])
def error_msg():

    ws = http.client.HTTPConnection(ws_host, timeout=10)
    headers = {"Content-Type": "application/json"}

    try:
        params = {
            "fromUserId": "homework",
            "msg": "\{\"test\"\}",
            "userIds": [1]
        }

        return_msg = {
            "type": "error",
            "content": "xxx 传感器超过阈值！！！！"
        }

        params["msg"] = json.dumps(return_msg)

        param_json = json.dumps(params, ensure_ascii=False)
        print(param_json)
        ws.request("POST", "/ws/sendMessage",
                    param_json, headers)

        r1 = ws.getresponse()
        # This will return entire content.
        data = r1.read().decode('utf8')
        print(data)
        ws.close()
    except Exception as e:
        print(e)
        ws.close()

    result = success_result.copy()
    result["msg"] = "发送消息成功"
    return jsonify(result)



@app.route('/api/sensordata/warning', methods=['GET','POST'])
def warning_msg():

    ws = http.client.HTTPConnection(ws_host, timeout=10)
    headers = {"Content-Type": "application/json"}

    try:
        params = {
            "fromUserId": "homework",
            "msg": "\{\"test\"\}",
            "userIds": [1]
        }

        return_msg = {
            "type": "warning",
            "content": "xxx 现在在浇水"
        }

        params["msg"] = json.dumps(return_msg)

        param_json = json.dumps(params, ensure_ascii=False)
        print(param_json)
        ws.request("POST", "/ws/sendMessage",
                    param_json, headers)

        r1 = ws.getresponse()
        # This will return entire content.
        data = r1.read().decode('utf8')
        print(data)
        ws.close()
    except Exception as e:
        print(e)
        ws.close()

    result = success_result.copy()
    result["msg"] = "发送消息成功"
    return jsonify(result)


# @app.route('/api/sensordata/realtimehttp', methods=['POST'])
# def http_realtime_sensordata():
#     greenhouse_id = request.json['greenhouse_id']

#     result = success_result.copy()
#     result["msg"] = "开始发送实时传感器数据"
#     return jsonify(result)


@app.route('/api/sensordata/stop', methods=['POST'])
def stop_realtime_sensordata():
    # greenhouse_id = request.json['greenhouse_id']

    global CURRENT_GREENHOUSE_ID
    CURRENT_GREENHOUSE_ID = None
    result = success_result.copy()
    result["msg"] = "停止发送发送实时传感器数据"
    return jsonify(result)
