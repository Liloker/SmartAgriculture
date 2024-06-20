## 0 项目概述

项目在线体验地址（推荐国内）：~~http://60.204.149.135~~ 原服务器已过期，新地址http://106.54.34.76

针对某个区的农产品大棚种植情况进行管理。

详见同路径下“项目报告”。

## 1 部署

正常网络环境下，使用IE、Firefox等浏览器输入IP地址：~~http://60.204.149.135~~ 即可访问系统。
ubuntu22.04
conda 23.3.1
Python-3.8.19
java -version
openjdk version "1.8.0_402"
OpenJDK Runtime Environment (build 1.8.0_402-8u402-ga-2ubuntu1~22.04-b06)
OpenJDK 64-Bit Server VM (build 25.402-b06, mixed mode)


## 2 使用/功能介绍

本系统有5个功能栏，分别为首页大屏、传感器管理、病虫害识别、大棚管理和农产品种植物管理。

后端项目启动smartalg/server.py,外层目录用于yolov5训练，使用~~python3.8~~ python3.8.19，`pip install -r requirements.txt`

```bash
SmartAgriculture
├── benchmarks.py
├── classify
│   ├── predict.py
│   ├── train.py
│   ├── tutorial.ipynb
│   └── val.py
├── data
│   ├── Argoverse.yaml
│   ├── coco128-seg.yaml
│   ├── coco128.yaml
│   ├── coco.yaml
│   ├── GlobalWheat2020.yaml
│   ├── hyps
│   ├── ImageNet.yaml
│   ├── images
│   ├── Objects365.yaml
│   ├── scripts
│   ├── SKU-110K.yaml
│   ├── VisDrone.yaml
│   ├── VOC.yaml
│   └── xView.yaml
├── detect.py
├── export.py
├── hubconf.py
├── __init__.py
├── LICENSE
├── models
│   ├── common.py
│   ├── experimental.py
│   ├── hub
│   ├── __init__.py
│   ├── __pycache__
│   ├── segment
│   ├── tf.py
│   ├── yolo.py
│   ├── yolov5l.yaml
│   ├── yolov5m.yaml
│   ├── yolov5n.yaml
│   ├── yolov5s.yaml
│   └── yolov5x.yaml
├── README.md
├── requirements.txt # yolov5要用的
├── runs
│   ├── detect
│   └── train
├── segment
│   ├── predict.py
│   ├── train.py
│   ├── tutorial.ipynb
│   └── val.py
├── setup.cfg
├── smartalg # 后端项目入口文件夹
│   ├── api.txt
│   ├── createdb.py
│   ├── dbfile
│   ├── farm_product.py
│   ├── flask_models.py
│   ├── greenhouse.py
│   ├── instance
│   ├── nohup.out
│   ├── product_cycle.py
│   ├── requirements.txt # 后端项目需要的
│   ├── results
│   ├── run.sh # 部署Linux时使用
│   ├── sensor_data.py
│   ├── sensor.py
│   ├── server.py # main入口
│   ├── smutils.py
│   ├── test_images
│   ├── upload.py
│   ├── uploads
│   ├── y_detect.py
│   ├── yolo_detect.py
│   └── yolo.doc
├── test
│   └── y_detect.py
├── train.py
├── tutorial.ipynb
├── utils
│   ├── activations.py
│   ├── augmentations.py
│   ├── autoanchor.py
│   ├── autobatch.py
│   ├── aws
│   ├── callbacks.py
│   ├── dataloaders.py
│   ├── docker
│   ├── downloads.py
│   ├── flask_rest_api
│   ├── general.py
│   ├── google_app_engine
│   ├── __init__.py
│   ├── loggers
│   ├── loss.py
│   ├── metrics.py
│   ├── plots.py
│   ├── __pycache__
│   ├── segment
│   ├── torch_utils.py
│   └── triton.py
├── val.py
├── yolov5s-seg.pt
└── yolov5.yaml

```





### 首页大屏

#### 显示

首页显示系统所管理的各个大棚的各项数据。

显示内容包括空气温度、空气湿度、二氧化碳浓度、光照度、土壤温度、土壤湿度。

数据以曲线图的形式呈现，其中横轴为日期，纵轴表示数据大小。

将鼠标放置在某项数据图中曲线上，可显示具体至某一秒的对应数值。

![](pic/首页大屏-显示.png)

#### 查询

页面上方查询栏可输入大棚编号和日期，搜索并在页面中下方显示指定大棚在指定日期内的数据。

### 传感器管理

![](pic/传感器管理-首页.png)

#### 显示

数据列表显示系统管理的各个传感器数据。

显示内容：包括传感器编号、传感器名称、传感器位置、传感器类型、所在大棚以及支持的操作。

#### 查询

可按位置筛选位于不同位置的传感器。

#### 编辑

支持对传感器的新增、编辑和删除。

新增传感器时，需要填入传感器的名称、类型、位置、所属大棚以及报警阈值。

对已添加的传感器同样可以通过编辑来修改上述填入的参数。

不需要该传感器时，点击删除即可去除此传感器信息。

### 病虫害识别

![](pic/病虫害识别-首页.png)

#### 显示

页面默认显示识别虫害的历史记录。

内容包括图片文件名、识别结果（有几只虫）、识别时间（日期和时间）、大棚名称以及支持的操作。

点击“浏览”，可浏览识别图片中具体的识别结果。

![](pic/病虫害识别-浏览.png)

#### 识别

可通过拖曳图片到识别框或点击上传选择虫害图片。系统对图片内虫害情况分析识别后会显示对应结果。

### 大棚管理

![](pic/大棚管理-首页.png)

#### 显示

数据列表显示系统管理的各个大棚数据。

显示内容：包括大棚编号、大棚名称、传感器数量三项。

#### 编辑

支持对大棚的新增、编辑和删除。

新增大棚时，填入大棚名称即可。

对已添加的大棚同样可以通过编辑来修改上述填入的参数。

不需要该大棚时，点击删除即可去除此大棚信息。

### 农产品种植物管理

![](pic/农产品管理-首页.png)

#### 显示

数据列表显示系统管理的各个农产品种植物数据。

显示内容包括农产品编号、农产品名称、最近时间点所在大棚以及支持的操作。

#### 查询

同传感器管理，可按位置筛选位于不同位置的农产品。

#### 编辑

支持对农产品的新增、编辑和删除。

新增：种植物时，需要填入农产品名称和所属大棚。

编辑：对已添加的农作物同样可以通过编辑来修改上述填入的参数。

删除：不需要该农作物时，点击删除即可去除此农作物信息。

查看：点击“查看”，可进入该农产品详细数据的页面。

![](pic/农产品管理-查看.png)

在此页面，可以查看某一农产品的生长周期、对应时间点，并进行管理。

支持新增、编辑和删除周期。



## 3 API

见smartalg路径下“API文档”。

