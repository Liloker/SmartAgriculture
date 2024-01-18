from flask import request
# from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from greenhouse import *
from sensor import *
from farm_product import *
from product_cycle import *
from sensor_data import *
from upload import *

import time
import json

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 54311


# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

# sockets = Sockets(app)



# @sockets.route('/api/sensordata')
# def sensordata_socket(ws):
#     message = ws.receive()
#     msg_json = json.loads(message)
#     greenhouse_id = msg_json["greenhouse_id"]
#     # 是否包含开始时间的检查，判断是获取实时数据还是历史数据
#     if msg_json.__contains__("start_date"):
#         # 历史数据的部分日期为  年月日时分秒
#         sd = msg_json["start_date"]
#         ed = msg_json["end_date"]

#         history = get_history_sensordata(greenhouse_id, sd, ed)
#         ws.send(json.dumps(history))

#     else:
#         # 实时数据的部分
#         while not ws.closed:
#             # message = ws.receive()
#             # print(message)
#             n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             x = random_generate_data()

#             sd = SensorData(greenhouse_id=greenhouse_id,
#                             carbon_dioxide=x['carbon_dioxide'],
#                             air_temperature=x['air_temperature'],
#                             air_moisture=x['air_moisture'],
#                             light_intensity=x['light_intensity'],
#                             soil_temperature=x['soil_temperature'],
#                             soil_moisture=x['soil_moisture']
#                             )

#             db.session.add(sd)
#             db.session.commit()

#             d = {"sensor_data": x, "ts": n, "greenhouse_id": greenhouse_id}
#             print(d)
#             ws.send(json.dumps(d))
#             time.sleep(1)





@app.route('/api')
def hello_world():
    return 'Hello World!'



if __name__ == '__main__':
    activate_job()

    app.run(host=LISTEN_HOST, port=LISTEN_PORT)

    # server = pywsgi.WSGIServer(
    #     (LISTEN_HOST, LISTEN_PORT), app, handler_class=WebSocketHandler)
    # print("serving flask socket at {}:{}".format(LISTEN_HOST, LISTEN_PORT))
    # server.serve_forever()
