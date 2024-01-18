from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
import datetime
import os

app = Flask(__name__)

# mysql部分的配置
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'smart_algriculture'
MYSQL_SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
    USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLITEDB_PATH = os.path.join(os.getcwd(),'dbfile/sa.db')
# sqlite相关的数据库配置
SQLITE_SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQLITEDB_PATH


# sqlite 配置数据库的连接参数, 默认使用sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

        

class Sensor(db.Model):
    __tablename__ = 't_sensor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    sensor_type = db.Column(db.String(64), nullable=False)
    position = db.Column(db.String(64), nullable=False)
    greenhouse_id = db.Column(db.Integer, db.ForeignKey(
        't_greenhouse.id'), nullable=False)
    alert_threshold = db.Column(db.Float(precision="10,2"), nullable=False)

    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)


class SensorData(db.Model):
    # json_encoder = JsonEncoder
    __tablename__ = 't_sensordata'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    greenhouse_id = db.Column(db.Integer, db.ForeignKey(
        't_greenhouse.id'), nullable=False)
    # carbon_dioxide
    carbon_dioxide = db.Column(db.Integer, nullable=False)
    air_temperature = db.Column(db.Integer, nullable=False)
    air_moisture = db.Column(db.Integer, nullable=False)
    light_intensity = db.Column(db.Integer, nullable=False)
    soil_temperature = db.Column(db.Integer, nullable=False)
    soil_moisture = db.Column(db.Integer, nullable=False)
    dt = db.Column(db.DateTime, default=datetime.datetime.now)  # 检测日期
    
    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]

        d = {}
        for c in columns:
            o = getattr(self, c)
            if c == "dt":
                o = o.strftime("%Y-%m-%d %H:%M:%S")
            d[c] = o
        return d


class Greenhouse(db.Model):
    __tablename__ = 't_greenhouse'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    sensors = db.relationship(
        'Sensor', backref=db.backref('greenhouse', lazy=False))
    farmproducts = db.relationship(
        'FarmProduct', backref=db.backref('greenhouse', lazy=False))
    pestinspections = db.relationship(
        'PestInspection', backref=db.backref('greenhouse', lazy=False))

    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)


class PestInspection(db.Model):
    __tablename__ = 't_pest_inspection'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.String(256), nullable=False)  # 图片名称
    path = db.Column(db.String(2048), nullable=False)  # 图片存储路径
    result_path = db.Column(db.String(2048), nullable=False)  # 结果图片存储路径
    rec_result = db.Column(db.String(256), nullable=False)  # 识别结果
    pest_num = db.Column(db.Integer, default=0)  # 虫子数量
    greenhouse_id = db.Column(db.Integer, db.ForeignKey(
        't_greenhouse.id'), nullable=False)
    rec_date = db.Column(db.DateTime, default=datetime.datetime.now)  # 检测日期
    
    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]

        d = {}
        for c in columns:
            o = getattr(self, c)
            if c == "rec_date":
                o = o.strftime("%Y-%m-%d %H:%M:%S")
            d[c] = o
        return d
    

#农产品类
class FarmProduct(db.Model):
    __tablename__ = 't_farm_product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    latest_date = db.Column(db.Date, nullable=True)  # 最近日期
    productcycles = db.relationship(
        'ProductCycle', backref=db.backref('farmproduct', lazy=False))
    greenhouse_id = db.Column(db.Integer, db.ForeignKey(
        't_greenhouse.id'), nullable=False)

    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        d = {}
        for c in columns:
            o = getattr(self, c)
            if o == None:
                o = ""
            elif type(o) == datetime.date:
                o = o.strftime("%Y-%m-%d")

            d[c] = o

        return d

#种植物生产周期类
class ProductCycle(db.Model):
    __tablename__ = 't_product_cycle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cycle_name = db.Column(db.String(256), nullable=True)
    date = db.Column(db.Date, nullable=True)  # 时间点
    farmproduct_id = db.Column(db.Integer, db.ForeignKey(
        't_farm_product.id'), nullable=False)

    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        d = {}
        for c in columns:
            o = getattr(self, c)
            if o == None:
                o = ""
            elif type(o) == datetime.date:
                o = o.strftime("%Y-%m-%d")

            d[c] = o
        return d
