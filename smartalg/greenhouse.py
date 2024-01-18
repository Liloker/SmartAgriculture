from flask import request, jsonify
from flask_models import *
from smutils import *


def list_gh():
    all_greenhouse = Greenhouse.query.all()

    data = []
    for gh in all_greenhouse:
        c = len(gh.sensors)
        d = gh.to_dict()
        d["count"] = c
        data.append(d)
    return data


@app.route('/api/greenhouse/list', methods=['GET', 'POST'])
def list_greenhouse():

    data = list_gh()

    result = success_result.copy()
    result["data"] = data
    return jsonify(result)


@app.route('/api/greenhouse/insert', methods=['POST'])
def insert_greenhouse():

    name = request.json['name']

    greenhouse = Greenhouse(name=name)
    db.session.add(greenhouse)
    db.session.commit()

    # data = list_gh()

    result = success_result
    # result["data"] = data
    return jsonify(result)


@app.route('/api/greenhouse/update', methods=['POST'])
def update_greenhouse():

    greenhouse_id = request.json["id"]
    new_name = request.json['name']

    greenhouse = Greenhouse.query.filter_by(id=greenhouse_id).first()
    if greenhouse == None:
        result = notfound_result.copy()
        # data = list_gh()
        result['msg'] = '没有找到对应的大棚'
        return jsonify(result)

    greenhouse.name = new_name
    db.session.commit()

    # data = list_gh()

    result = success_result
    # result["data"] = data
    return jsonify(result)


# 删除按钮-tested
@app.route('/api/greenhouse/delete', methods=['POST'])
def delete_greenhouse():
    greenhouse_id = request.json["id"]
    greenhouse = db.session.query(Greenhouse).filter(
        Greenhouse.id == greenhouse_id).first()
    if greenhouse is None:
        return jsonify(notfound_result)

    # 删除该温室下的所有传感器
    for sensor in greenhouse.sensors:
        db.session.delete(sensor)
    db.session.delete(greenhouse)
    db.session.commit()
    return jsonify(success_result)
