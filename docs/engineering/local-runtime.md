# d2c-backoffice-api 本地运行说明

本文档记录 D2C 商家中台后端第一阶段本地运行合同。

service_name = d2c-backoffice-api
app_code = d2c-backoffice
service_client_code = d2c-backoffice-service
api_path = /api/d2c-backoffice
web_path = /backoffice
local_api_port = 8026
local_web_port = 5288

## 启动

cd ~/d2c-backoffice-api
make install
make upgrade-dev
make alembic-check
make uvicorn-up

## 健康检查

curl -s http://127.0.0.1:8026/system/health | python3 -m json.tool

## 停止

cd ~/d2c-backoffice-api
make uvicorn-down

## 当前阶段边界

第一刀只搭独立后端、独立数据库、健康检查、OpenAPI、Alembic 和 CI。

不迁移：

- /backoffice/pages/*
- /backoffice/catalog/*
- /backoffice/promotion-rules/*
- 商品表
- 价格表
- 促销表
- 优惠券表
- 页面注册表

## 页面目录

第二阶段起，商家中台页面目录接口由 d2c-backoffice-api 提供：

- GET /backoffice/pages/health
- GET /backoffice/pages/registry
- GET /backoffice/pages/navigation

调用方仍需传入：

X-Backoffice-Client: d2c-backoffice
