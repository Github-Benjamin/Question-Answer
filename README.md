
# Python web.py框架开发WEB问答平台


配置相关：

1. 安装并创建相关数据库，运行SQL脚本>question.sql 

2. 后续内容请自行脑补......

3. PyCharm-Github-Git实现代码版本管理，公司与家庭代码同步（2017-8-17）



#uWSGI项目部署简介：

1. Py文件：application = web.application(urls,globals()).wsgifunc()
2. 启动命令：uwsgi --http :8000 --module login

备注：login为配置py文件名称
