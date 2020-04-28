## HPLC Plot

### 项目要求

使用高斯混合分布来模拟液相色谱仪（HPLC）的图像生成，并参照ChemStation风格作图



### 项目说明

#### A. 内容

1. 根据高斯分布参数作图
2. 使用参数控制方法控制图像设置
3. 部署到服务器使用浏览器交互



#### B. 方法

1. 采用matplotlib作为画图工具库
2. 前端采用bootstrap4框架，后端采用tornado框架



### 目录文件说明

* hplc_server.py：后端响应程序主文件
* hplc.py：主作图文件
* debug.py：调试文件
* SIGNAL01.cdf：溶剂峰数据来源
* statics：前端静态文件（tornado）
* template：前端网页模版（tornado）



### 项目部署

我采用的是Nginx + Tornado进行服务器部署，Nginx负责请求的端口转发，Tornado监听转发端口以处理请求并返回，Nginx具体部署细节可自行google，Tornado部分只需要直接运行hplc_server.py即可