
from flask import request, jsonify
from flask_models import *
from smutils import *


# ============================农产品种植物管理===============================

# 新增种植物-tested
# json示例 {"name":"胡萝卜","latest_date":"2023-03-01","greenhouse_name":"西部三号温室"}
@app.route('/api/farmproduct/insert', methods=["POST"])
def insert_farmproduct():
    greenhouse_id = request.json['greenhouse_id']
    name = request.json['name']

    greenhouse = Greenhouse.query.filter_by(id=greenhouse_id).first()
    if greenhouse == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的大棚信息"
        return jsonify(result)

    farmproduct = FarmProduct(
        name=name, latest_date=None, greenhouse_id=greenhouse_id)
    db.session.add(farmproduct)
    db.session.commit()
    return jsonify(success_result)


# 删除按钮-tested
@app.route('/api/farmproduct/delete', methods=['POST'])
def delete_farmproduct():
    farmproduct_id = request.json['id']

    farmproduct: FarmProduct = FarmProduct.query.filter_by(
        id=farmproduct_id).first()
    if farmproduct == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的农产品种植物"
        return jsonify(result)

    # 级联删除 productcycle
    for productcycle in farmproduct.productcycles:
        db.session.delete(productcycle)

    db.session.delete(farmproduct)
    db.session.commit()
    return jsonify(success_result)

# 编辑按钮-tested
@app.route('/api/farmproduct/update', methods=['POST'])
def update_farmproduct():

    farmproduct_id = request.json['id']
    greenhouse_id = request.json['greenhouse_id']
    name = request.json['name']

    farmproduct: FarmProduct = FarmProduct.query.filter_by(
        id=farmproduct_id).first()
    if farmproduct == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的农产品种植物"
        return jsonify(result)

    greenhouse = Greenhouse.query.filter_by(id=greenhouse_id).first()
    if greenhouse == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的大棚"
        return jsonify(result)

    farmproduct.name = name
    farmproduct.greenhouse_id = greenhouse_id
    db.session.commit()

    return jsonify(success_result)


# 种植物列表-tested
@app.route('/api/farmproduct/list', methods=['GET', 'POST'])
def list_farmproduct():
    farmproducts = FarmProduct.query.all()
    data = []
    for s in farmproducts:
        d = s.to_dict()
        d['greenhouse_name'] = s.greenhouse.name
        data.append(d
                    # {
                    #     'id': s.id,
                    #     'name': s.name,
                    #     'latest_date': s.latest_date,
                    #     'greenhouse_name': s.greenhouse_name
                    # }
                    )
    result = success_result.copy()
    result["data"] = data
    return jsonify(result)
