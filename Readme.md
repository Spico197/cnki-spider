# 重构说明

---

[TOC]

---


## 爬虫

### 通过搜索得出具体期刊

1. 返回所有的待选项编号和名称
2. 人工选择待选项, 找到对应的`pcode`和`pykm(baseid)`字段

### 年份卷号爬取

1. 先找到`div class="pagelist"`, 将页码中的全部页码信息取出;
2. 根据上述得到的`pagelist`确定`pageindex`. `pagelist`中的页码从0开始, `pageindex`中的页码从1开始. 注意区分.
3. 获取其中所有的`年份`+`卷标`信息, 并返回.

### 论文网页名爬取

1. 从`http://navi.cnki.net/KNavi/JournalDetail?pcode=CJFD&pykm=GZDI&year=2017&issue=03`类似的网页抓取论文编号, 组成`year+issue+list_number`字段

### 论文具体内容爬取

1. 构建`host`请求地址, `http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=GZDI198201000`, 其中`filename`的部分即为`GZDI`+ year+issue+文章序号.
2. 爬取题目, 作者, 单位, 基金, 关键词, 摘要, DOI, 下载数, 页码, 页数, 大小等信息

## 项目管理

## 数据库连接

## 数据可视化

## GUI设计

