from flask import request, jsonify
from flask_models import *
from smutils import *


def list_s(all_sensors=None):
    if all_sensors == None:
        all_sensors = Sensor.query.all()

    data = []
    for sensor in all_sensors:
        d = sensor.to_dict()
        d['greenhouse_name'] = sensor.greenhouse.name
        data.append(d)
    return data

@app.route('/api/sensor/listtype', methods=['GET','POST'])
def list_sensor_type():
    data = [
        "空气温度传感器",
        "空气湿度传感器",
        "土壤温度传感器",
        "土壤湿度传感器",
        "光照传感器",
        "二氧化碳浓度传感器"
    ]
    result = success_result.copy()
    result["data"] = data
    return jsonify(result)

@app.route('/api/sensor/list', methods=['GET','POST'])
def list_sensor():
    data = []

    if request.data.decode('utf-8') != '' and request.is_json and request.json.__contains__("greenhouse_id"):
        greenhouse_id = request.json['greenhouse_id']
    
        greenhouse = Greenhouse.query.filter_by(id=greenhouse_id).first()
        if greenhouse == None:
            result = notfound_result.copy()
            result['msg'] = "没有找到对应的大棚信息"
            # result['data'] = list_s()
            return jsonify(result)
        
        sensors = Sensor.query.filter_by(greenhouse_id=greenhouse_id).all()

        data = list_s(sensors)
    else:
        data = list_s()

    result = success_result.copy()
    result["data"] = data
    return jsonify(result)


@app.route('/api/sensor/insert', methods=['POST'])
def insert_sensor():

    name = request.json['name']
    sensor_type = request.json['sensor_type']
    position = request.json['position']
    greenhouse_id = request.json['greenhouse_id']
    alert_threshold = request.json['alert_threshold']


    greenhouse = Greenhouse.query.filter_by(id=greenhouse_id).first()
    if greenhouse == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的大棚信息"
        # result['data'] = list_s()
        return jsonify(result)


    sensor = Sensor(name=name, sensor_type=sensor_type, position=position,
                    alert_threshold=alert_threshold, greenhouse_id=greenhouse_id)
    db.session.add(sensor)
    db.session.commit()

    # data = list_s()

    result = success_result
    # result["data"] = data
    return jsonify(result)



# 编辑按钮-tested
@app.route('/api/sensor/update', methods=['POST'])
def update_sensor():

    sensor_id = request.json['id']
    name = request.json['name']
    sensor_type = request.json['sensor_type']
    position = request.json['position']
    greenhouse_id = request.json['greenhouse_id']
    alert_threshold = request.json['alert_threshold']

    sensor = Sensor.query.filter_by(id=sensor_id).first()
    if sensor == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的传感器信息"
        # result['data'] = list_s()
        return jsonify(result)


    greenhouse = Greenhouse.query.filter_by(id=greenhouse_id).first()
    if greenhouse == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的大棚信息"
        # result['data'] = list_s()
        return jsonify(result)
    
    sensor.name = name
    sensor.sensor_type = sensor_type
    sensor.position = position
    sensor.greenhouse_id = greenhouse_id
    sensor.alert_threshold = alert_threshold
    db.session.commit()

    # data = list_s()

    result = success_result
    # result["data"] = data
    return jsonify(result)




# 删除按钮-tested
@app.route('/api/sensor/delete', methods=['POST'])
def delete_sensor():
    sensor_id = request.json['id']
    sensor = db.session.query(Sensor).filter(Sensor.id == sensor_id).first()
    
    if sensor == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的传感器信息"
        # result['data'] = list_s()
        return jsonify(result)
    
    db.session.delete(sensor)
    db.session.commit()

    # data = list_s()

    result = success_result
    # result["data"] = data
    return jsonify(result)



# 按位置筛选传感器-tested
@app.route('/api/sensor/filter', methods=['POST'])
def filter_sensor():
    greenhouse_id = request.json['greenhouse_id']
    
    greenhouse = Greenhouse.query.filter_by(id=greenhouse_id).first()
    if greenhouse == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的大棚信息"
        # result['data'] = list_s()
        return jsonify(result)
    
    sensors = Sensor.query.filter_by(greenhouse_id=greenhouse_id).all()
    
    data = list_s(sensors)
    result = success_result.copy()
    result["data"] = data
    return jsonify(result)