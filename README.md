### 由于不信任第三方的地址解析、转换服务，加上想定制自己的规则与策略组，于是有了此项目
 - 整合[lhie1](https://github.com/lhie1/Rules)规则和自用的一些规则
 - 整合自用的`Proxy Group`
 - 解析`vmess`订阅成`clash`订阅
 - 流水线定时更新规则提供给`clash`（`vmess`订阅地址存储于`Secret`中）