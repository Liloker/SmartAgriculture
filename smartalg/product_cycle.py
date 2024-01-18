
from flask import request, jsonify
from flask_models import *
from smutils import *

# ============================种植物生产周期管理=========================


def update_latest_to_farmproduct(farmproduct: FarmProduct):

    productcycles = farmproduct.productcycles
    if len(productcycles) == 0:
        farmproduct.latest_date = None
        db.session.commit()
        return

    sort = sorted(productcycles, key=lambda r: r.date if r.date !=
                  None else datetime.date.max)
    latest_productcycle = sort[0]
    farmproduct.latest_date = latest_productcycle.date
    db.session.commit()

# 生产周期列表-tested


@app.route('/api/productcycle/list', methods=['POST'])
def list_productcycle():
    farmproduct_id = request.json["farmproduct_id"]

    farmproduct = FarmProduct.query.filter_by(id=farmproduct_id).first()
    if farmproduct == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的农产品种植物"
        return jsonify(result)

    productcycles = ProductCycle.query.filter_by(
        farmproduct_id=farmproduct_id).order_by(ProductCycle.date.asc())
    data = []
    other = []
    for pc in productcycles:
        d = pc.to_dict()
        if d["date"] == "":
            other.append(d)
        else:
            data.append(d)

    # 新加的往后面排
    other.extend(data)
    result = success_result.copy()
    result["data"] = other
    return jsonify(result)


# 新增周期-tested
@app.route('/api/productcycle/insert', methods=["POST"])
def insert_productcycle():
    farmproduct_id = request.json["farmproduct_id"]
    cycle_name = request.json['cycle_name']
    date_str = request.json['date']
    # date = datetime.strptime(date_str, '%Y-%m-%d').date()
    farmproduct = FarmProduct.query.filter_by(id=farmproduct_id).first()
    if farmproduct == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的农产品种植物"
        return jsonify(result)

    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    productcycle = ProductCycle(
        farmproduct_id=farmproduct_id, cycle_name=cycle_name, date=date)
    db.session.add(productcycle)
    db.session.commit()

    # 更新最新生产周期时间
    update_latest_to_farmproduct(farmproduct)

    return jsonify(success_result)


# 删除按钮-tested
@app.route('/api/productcycle/delete', methods=['POST'])
def delete_productcycle():
    productcycle_id = request.json['productcycle_id']
    productcycle = ProductCycle.query.filter_by(id=productcycle_id).first()
    if productcycle == None:
        res = notfound_result.copy()
        res["msg"] = "没有找到对应的农产品生产周期"
        return jsonify(res)

    db.session.delete(productcycle)
    db.session.commit()

    # 更新最新生产周期时间
    update_latest_to_farmproduct(productcycle.farmproduct)

    return jsonify(success_result)


# 保存按钮-tested
# json示例 {"cycle_name":"开花","date":"2023-03-29"}
@app.route('/api/productcycle/update', methods=['POST'])
def update_productcycle():
    productcycle_id = request.json['id']
    cycle_name = request.json['cycle_name']
    date_str = request.json['date']

    productcycle = ProductCycle.query.filter_by(id=productcycle_id).first()
    if productcycle == None:
        res = notfound_result.copy()
        res["msg"] = "没有找到对应的农产品生产周期"
        return jsonify(res)

    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    productcycle.cycle_name = cycle_name
    productcycle.date = date
    db.session.commit()

    # 更新最新生产周期时间
    update_latest_to_farmproduct(productcycle.farmproduct)

    return jsonify(success_result)
