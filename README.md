# d2c-backoffice-api

d2c-backoffice-api 是 D2C 商家中台后端服务。

第一阶段只搭独立后端底座，不迁移业务表，不接管商品、价格、促销或页面注册能力。

## 本地合同

service_name: d2c-backoffice-api
app_code: d2c-backoffice
service_client_code: d2c-backoffice-service
api_path: /api/d2c-backoffice
web_path: /backoffice
local_api_port: 8026
local_web_port: 5288
local_database: postgresql+psycopg://d2c_backoffice:d2c_backoffice@127.0.0.1:5433/d2c_backoffice

## 启动命令

cd ~/d2c-backoffice-api
make install
make upgrade-dev
make alembic-check
make check
make uvicorn-up
make uvicorn-status
make uvicorn-logs
make uvicorn-down

## 当前边界

第一阶段只建立独立后端和独立数据库底座。

暂不迁移：

- /backoffice/pages/*
- /backoffice/catalog/*
- /backoffice/promotion-rules/*
- 商品表
- 价格表
- 促销表
- 优惠券表
- 页面注册表

## 当前已接入能力

- GET /system/health
- GET /backoffice/pages/health
- GET /backoffice/pages/registry
- GET /backoffice/pages/navigation

/backoffice/pages/* 已迁入 d2c-backoffice-api，页面目录表归 d2c_backoffice_db。
