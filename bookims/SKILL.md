---
name: bookims
description: 湖南云立方科技提供的线下书屋图书管理进销存系统,图因IMS,用来响应用户的进销存操作请求,如查询库存,查询某本书是否存在,以及统计库存信息,销售情况等
version: 1.0.0
---
# 获得accessToken授权

运行  gettoken.py文件中的get_access_token函数,获得返回值
```python
def get_access_token()
```

# 商品进销存管理

## 商品库存查询

根据书本名称查询库存中该书的数量
输入参数:
title: 书本名称
TURINGDANCE_BOOKIMS_HOST: 从环境变量中获得
TOKEN: 调用 get_access_token 方法获得

```bash
curl -v -H "Authorization: Bearer ${TOKEN}" "${TURINGDANCE_BOOKIMS_HOST}/bookims/stock/getMineByTitle?title=${title}"
```

输出结构如下
```json
{"code":200,rows:[{"quantity":"剩余数量","book":{"title":"书的名称"},"shelf":{"name":"所造货架号"}}]}
```
如果失败则返回如下结构
```json
{"code":"错误码","msg":"错误原因"}
```

根据以上返回组织内容,格式如下

书本名称: book.title
当前数量: quantity
所在货架: shelf.name


## 销售信息统计

查询今天的销售情况
输入参数:
title: 书本名称
TURINGDANCE_BOOKIMS_HOST: 从环境变量中获得
TOKEN: 调用 get_access_token 方法获得
bizcode: 具体统计指标,可选择信息如下:

bkimsquantityofcktoday	今日销售本数
bkimsamountofcktody	今日销售金额
bkimsquantityofstock	当前压货数量
bkimsamountofstock	当前压货金额

```bash
curl -v -H "Authorization: Bearer ${TOKEN}" "${TURINGDANCE_BOOKIMS_HOST}/report/rule/excutemine/${bizcode}"
```
比如用户需要查询 今日销售本数,则bizcode=bkimsquantityofcktoday,最终调用如下
```bash
curl -v -H "Authorization: Bearer ${TOKEN}" "${TURINGDANCE_BOOKIMS_HOST}/report/rule/excutemine/bkimsquantityofcktoday"
```

输出结构如下
```json
{"code":200,"data":"返回的统计数据"}
```
如果失败则返回如下结构
```json
{"code":"错误码","msg":"错误原因"}
```


## 店铺经营情况

分别处理如下统计信息

bkimsquantityofcktoday	今日销售本数
bkimsamountofcktody	今日销售金额
bkimsquantityofstock	当前压货数量
bkimsamountofstock	当前压货金额

然后汇总成报表

## 商品情况报表
获得商品整体情况汇报,包括累计销售情况,累计进货情况,库存情况,最近30天销售情况
可选参数
timeBefore: 查询销售时间发生在该时间点以前的商品情况,非必须,格式必须满足 YYYY-MM-DD HH:ii:SS 的形式,如 2023-03-13 14:25:49
timeAfter: 查询销售时间发生在该时间点以后的商品情况,非必须,格式必须满足 YYYY-MM-DD HH:ii:SS 的形式,如 2023-03-13 14:25:49
order: 排序方式可选 asc/desc
prop:  排序字段,可选字段及含义如下
    - qtyStockinTotal: 按照入库数量
    -  qtySaleoutTotal: 按照出库数量
    -  amtStockinTotal: : 按照入库金额,统计成本时候需要
    -  amtSaleoutTotal: 按照出库金额
    -  qtySaleoutDay30: 最近30天的出货数量
    -  amtSaleoutDay30: 最近30天的出货金额

pegeSize: 需要拉取多少条记录

脚本请求如下
```bash
curl -v -H "Authorization: Bearer ${TOKEN}" "${TURINGDANCE_BOOKIMS_HOST}/bookims/rptbook/listMine"
```

输出结构如下
```json
{"code":200,rows:[
    {"qtyStockinTotal":"入库数量","qtySaleoutTotal":"出库数量","amtStockinTotal":"入库金额","amtSaleoutTotal":"出库金额",
    "qtySaleoutDay30":"最近30天出货数量","amtSaleoutDay30":"最近30天出库金额",
    "qtyStocked":"当前库存数量",
    "amtStocked":"当前库存金额",
    "book":{"title":"书的名称","isbn":"书得isbn信息","cover":"书的图片链接"}}]
}
```
如果失败则返回如下结构
```json
{"code":"错误码","msg":"错误原因"}
```

## 商品销售情况报表
列举出发生在时间区间内的商品销售情况
可选参数
timeBefore: 统计销售时间发生在该时间点以前的商品情况,不关注请不要传递,格式必须满足 YYYY-MM-DD HH:ii:SS 的形式,如 2023-03-13 14:25:49
timeAfter: 统计发生在该时间点以后的商品销售情况,不关注请不要传递,格式必须满足 YYYY-MM-DD HH:ii:SS 的形式,如 2023-03-13 14:25:49
脚本请求如下
```bash
curl -v -H "Authorization: Bearer ${TOKEN}" "${TURINGDANCE_BOOKIMS_HOST}/bookims/rptbook/listMyRealTimeSalesByIsbn"
```

输出结构如下
```json
{"code":200,rows:[
    {
    "quantity":"当前销售数量",
    "amount":"当前销售金额",
    "isbn":"商品的ISBN信息",
    "book":{"title":"书的名称","isbn":"书得isbn信息","cover":"书的图片链接"}}]
}
```
如果失败则返回如下结构
```json
{"code":"错误码","msg":"错误原因"}
```