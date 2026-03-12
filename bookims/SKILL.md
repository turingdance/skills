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


## 店铺经验情况

分别处理如下统计信息

bkimsquantityofcktoday	今日销售本数
bkimsamountofcktody	今日销售金额
bkimsquantityofstock	当前压货数量
bkimsamountofstock	当前压货金额

然后汇总成报表