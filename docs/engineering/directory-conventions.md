# d2c-backoffice-api 目录与命名规范

d2c-backoffice-api 是 D2C 商家中台后端，不承载顾客前台运行时。

## 目录原则

app/api/routes/          HTTP 路由
app/core/                配置、数据库、基础设施
app/domains/<domain>/    后续业务领域
app/domains/<domain>/models
app/domains/<domain>/repos
app/domains/<domain>/contracts
app/domains/<domain>/services

第一刀暂不创建业务领域目录，避免把商品、价格、促销提前迁入。

## 命名原则

- backoffice 表示商家中台 / 经营后台。
- storefront 表示顾客前台，不应出现在本服务的业务 runtime owner 中。
- internal/read/v1 后续只用于服务间读取，不给浏览器直接调用。
- admin 暂不用于商家经营后台。
