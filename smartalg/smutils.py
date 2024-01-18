import random
from flask_models import *
from sqlalchemy import and_

success_result = {
    "status": 200,
    "msg": "success",
    "data": {}
}

notfound_result = {
    "status": 404,
    "msg": "查找的实体不存在",
    "data": {}
}

def get_history_sensordata(gid, sd, ed):
    history = db.session.query(SensorData).filter(and_(SensorData.greenhouse_id == gid,
                                                  SensorData.dt.between(sd, ed))).order_by(SensorData.dt.desc()).limit(20)
    l = [x.to_dict() for x in history]
    return l


def random_generate_data():

    # 二氧化碳浓度：1500ppm-3000ppm
    carbon_dioxide = random.randrange(1500, 3000, 1)
    # 室温 摄氏度
    air_temperature = random.randrange(0, 40, 1)
    # 湿度 百分比
    air_moisture = random.randrange(1, 100, 1)
    # 光照度 范围 0-100klux
    light_intensity = random.randrange(0, 100, 1)

    # 土壤温度 0-30 摄氏度
    soil_temperature = random.randrange(0, 30, 1)
    # 土壤湿度 0-100 百分比
    soil_moisture = random.randrange(0, 100, 1)

    print(carbon_dioxide, air_temperature, air_moisture,
          light_intensity, soil_temperature, soil_moisture)
    d = {
        "carbon_dioxide": carbon_dioxide,
        "air_temperature": air_temperature,
        "air_moisture": air_moisture,
        "light_intensity": light_intensity,
        "soil_temperature": soil_temperature,
        "soil_moisture": soil_moisture
    }
    return d
    # return (carbon_d, air_temperature, air_moisture, light_intensity, soil_temperature, soil_moisture)


def convert_orm_to_showing_sensor_data(sensor_data_list):

    return_msg = {
        "chat1": {
            "columns": ['日期', '空气温度'],
            "rows": [
            ]
        },

        "chat2": {
            "columns": ['日期', '空气湿度'],
            "rows": [
            ]
        },

        "chat3": {
            "columns": ['日期', '二氧化碳浓度'],
            "rows": [
            ]
        },

        "chat4": {
            "columns": ['日期', '光照度'],
            "rows": [
            ]
        },

        "chat5": {
            "columns": ['日期', '土壤温度'],
            "rows": [
            ]
        },

        "chat6": {
            "columns": ['日期', '土壤湿度'],
            "rows": [
            ]
        }
    }

    chat1_rows = []  # 空气温度
    chat2_rows = []  # 空气湿度
    chat3_rows = []  # 二氧化碳浓度
    chat4_rows = []  # 光照度
    chat5_rows = []  # 土壤温度
    chat6_rows = []  # 土壤湿度
    # carbon_dioxide=x['carbon_dioxide'],
    # air_temperature=x['air_temperature'],
    # air_moisture=x['air_moisture'],
    # light_intensity=x['light_intensity'],
    # soil_temperature=x['soil_temperature'],
    # soil_moisture=x['soil_moisture']
    for sensor_data in sensor_data_list:
        # dt = sensor_data.dt.strftime("%Y-%m-%d %H:%M:%S")
        dt = sensor_data["dt"]
        d1 = {"日期": dt, "空气温度": sensor_data['air_temperature']}
        chat1_rows.append(d1)

        d2 = {"日期": dt, "空气湿度": sensor_data['air_moisture']}
        chat2_rows.append(d2)

        d3 = {"日期": dt, "二氧化碳浓度": sensor_data['carbon_dioxide']}
        chat3_rows.append(d3)

        d4 = {"日期": dt, "光照度": sensor_data['light_intensity']}
        chat4_rows.append(d4)

        d5 = {"日期": dt, "土壤温度": sensor_data['soil_temperature']}
        chat5_rows.append(d5)

        d6 = {"日期": dt, "土壤湿度": sensor_data['soil_moisture']}
        chat6_rows.append(d6)

    return_msg['chat1']['rows'] = chat1_rows
    return_msg['chat2']['rows'] = chat2_rows
    return_msg['chat3']['rows'] = chat3_rows
    return_msg['chat4']['rows'] = chat4_rows
    return_msg['chat5']['rows'] = chat5_rows
    return_msg['chat6']['rows'] = chat6_rows
    return return_msg


random_generate_data()
