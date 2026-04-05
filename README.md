# 题面
好的特征往往会显著提升策略收益。
在本题中, 希望你能根据下面的输入, 在规定时间内，倒推出特征的代码实现方式。

## 输入
- A股深交所股票行情数据
    - 以date/symbol存储的二进制行情文件
- 特征矩阵 (见ground_truth)
- 示例代码&框架 (src/**, 你可以在此基础上进行修改和实现)
    - 提供**output_1**作为example
    - 如果不使用预先准备的框架, 请在文档描述你代码的使用方式
- 深交所交易文档

## 输出
- 特征矩阵的实现代码(见src/sample.cpp), 不限制语言, 但使用c++实现会是加分项
- 说明文档，记录你的研究/实现过程/最终得分

## 运行方式
```bash
# 在 feature-research 目录下跑以下命令
# 打分脚本见 score.py
sh run.sh
```

## 得分计算方式
score=sum(每个矩阵的准确率 * 得分权重)/sum(总加权点数)
- 要求精度1e-6

| 匿名名称 | 得分权重 |
| --- | --- |
| output_1 | 0 |
| output_2 | 0 |
| output_3 | 2 |
| output_4 | 3 |
| output_5 | 1 |
| output_6 | 1 |
| output_7 | 1 |
| output_8 | 2 |
| output_9 | 3 |
| output_10 | 3 |
| output_11 | 3 |
| output_12 | 3 |
| output_13 | 3 |
| output_14 | 3 |
| output_15 | 3 |
| output_16 | 3 |
| output_17 | 3 |

## 评测环境
- linux 5.14.0
- gcc 11.4.1
- python 3.14

## 行情结构说明
order和trade数据放到了一起, 以**mdtype**作为区分

### Insert
| 字段 | 说明 |
| --- | --- |
| symbol | 标的名称 |
| exchange_timestamp | 交易所时间戳 |
| exchange_time | 交易所时间 |
| oid | 订单ID |
| seq | 事件发生的顺序 |
| price | 订单价格 |
| volume | 订单数量 |
| side | 买卖方向 |
| type | 订单类型 限价单: 50, 市价单: 49/85 |

### Cancel
| 字段 | 说明 |
| --- | --- |
| symbol | 标的名称 |
| exchange_timestamp | 交易所时间戳 |
| exchange_time | 交易所时间 |
| oid | 订单ID |
| seq | 事件发生的顺序 |
| volume | 订单数量 |

### Trade
| 字段 | 说明 |
| --- | --- |
| symbol | 标的名称 |
| exchange_timestamp | 交易所时间戳 |
| exchange_time | 交易所时间 |
| price | 成交价格 |
| volume | 成交数量 |
| side | 主动买卖方向 |
| seq | 事件发生的顺序 |
| buy_oid | 买方订单ID |
| sell_oid | 卖方订单ID |

# Tips
- 鼓励使用AI工具
- 请勿修改评测代码
- 评测环境有额外要求可以写明
- utils.py提供了python读取数据的方式