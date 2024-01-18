
from flask import request, jsonify, make_response
from flask_models import *
from smutils import *
from y_detect import *
import base64


@app.route('/api/upload/list', methods=['GET', 'POST'])
def list_upload():
    pestinspections = PestInspection.query.order_by(PestInspection.rec_date.desc()).all()
    data = []
    for pi in pestinspections:
        d = pi.to_dict()
        d['greenhouse_name'] = pi.greenhouse.name if pi.greenhouse != None else ""
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


@app.route('/api/upload/viewimg', methods=['POST'])
def viewimg_upload():
    pi_id = request.json["id"]
    pi = PestInspection.query.filter_by(id=pi_id).first()
    if pi == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的病虫害识别记录"
        return jsonify(result)

    result_path = pi.result_path

    f = open(result_path, "rb")
    image = f.read()
    # 创建response对象
    resp = make_response(image)
    # 设置response的headers对象
    resp.headers['Content-Type'] = 'image/jpeg'
    # resp.headers['image-focus'] = image_focus
    return resp

    # res = success_result.copy()
    # res['data'] = image_b64

    # return jsonify(res)


@app.route('/api/upload/viewb64', methods=['POST'])
def viewb64_upload():
    pi_id = request.json["id"]
    pi = PestInspection.query.filter_by(id=pi_id).first()
    if pi == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的病虫害识别记录"
        return jsonify(result)

    result_path = pi.result_path
    image_b64 = get_b64_image(result_path)
    res = success_result.copy()
    res['data'] = image_b64

    return jsonify(res)


@app.route('/api/upload/delete', methods=['POST'])
def delete_upload():
    pi_id = request.json["id"]
    pi = PestInspection.query.filter_by(id=pi_id).first()
    if pi == None:
        result = notfound_result.copy()
        result['msg'] = "没有找到对应的病虫害识别记录"
        return jsonify(result)

    db.session.delete(pi)
    db.session.commit()
    return jsonify(success_result)


@app.route('/api/upload/rec', methods=['POST'])
def rec_upload():
    img = request.files.get('image')
    greenhouse_id = request.form.get("greenhouse_id")

    save_path = "uploads/" + img.filename
    img.save(save_path)
    print(save_path)

    outputpath, target = recognize(save_path)
    print(outputpath)
    print(target)

    rec_result = ",".join(target)

    # image_name = db.Column(db.String(256), nullable=False)  # 图片名称
    # path = db.Column(db.String(2048), nullable=False)  # 图片存储路径
    # result_path = db.Column(db.String(2048), nullable=False)  # 结果图片存储路径
    # rec_result = db.Column(db.String(256), nullable=False)  # 识别结果
    # pest_num = db.Column(db.Integer, default=0)  # 虫子数量
    # greenhouse_id = db.Column(db.Integer, db.ForeignKey(
    #     't_greenhouse.id'), nullable=False)
    # rec_date = db.Column(db.DateTime, default=datetime.datetime.now)  # 检测日期
    pest_num = len(target)
    pi = PestInspection(image_name=img.filename, path=save_path,
                        result_path=outputpath, rec_result=rec_result, greenhouse_id=greenhouse_id, pest_num=pest_num)
    db.session.add(pi)
    db.session.commit()

    b64 = get_b64_image(outputpath)

    d = {"output_path": outputpath, "target": target, "result_image_b64": b64}
    result = success_result.copy()
    result['data'] = d

    return jsonify(result)


def get_b64_image(path):
    f = open(path, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read()).decode('ascii') # 读取文件内容，转换为base64编码
    f.close()
    return ls_f
