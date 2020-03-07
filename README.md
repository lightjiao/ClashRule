### 由于不信任第三方的地址解析、转换服务，加上想定制自己的规则与策略组，于是有了此项目
 - 整合[lhie1](https://github.com/lhie1/Rules)规则和自用的一些规则
 - 根据`Proxy`名字的关键字分成不同地区的`Proxy Group`
 - 专门将`bilibili`独立成一个`Proxy Group`
 
### Github Actions
 - 每晚 `20:00(UTC+8)🕗` 检查[lhie1](https://github.com/lhie1/Rules) 的`master`分支`/Clash/Rule.yaml`文件最近一天是否有`commit`
    - 如果有，则`actions`会以`233`为退出码，触发 `actions` 的通知，以提醒更新订阅
    
### 如何使用
#### 安装python依赖 
 ```bash
pip install requests
pip install PyYAML
pip install flask
```
#### 启动服务
```bash
python ./vmess-app.py
# 默认服务地址是 127.0.0.1:5000
```
#### 订阅链接
```bash
http://127.0.0.1:5000/?vmess=%VMESS_SUBSCRIBE_URL%
# VMESS_SUBSCRIBE_URL 为vmess订阅链接，记得url encode
```

