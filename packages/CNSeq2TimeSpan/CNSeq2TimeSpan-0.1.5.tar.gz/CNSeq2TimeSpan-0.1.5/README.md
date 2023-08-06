## CNSeq2TimeSpan
此项目基于[zhanzecheng的Time_NLP](https://github.com/zhanzecheng/Time_NLP),并增添了时间域的输出。

## Install
```shell script
pip install CNSeq2TimeSpan
```

## Examples
```python
from CNSeq2TimeSpan.TimeNormalizer import TimeNormalizer
tn = TimeNormalizer()

res = tn.parse(target=u'今年的财务报表交了吗')
print(res)

res = tn.parse(target=u'昨天刚写完，明天早上就交')
print(res)
```
返回结果
```json
{
	'timebase': '2019-11-21-15-3-58',
	'word': ['今年'],
	'type': 'timespan',
	'timespan': [
		['2019-01-01 00:00:00', '2019-12-31 23:59:59']
	]
}

{
	'timebase': '2019-11-21-8-3-58',
	'word': ['昨天', '明天早上'],
	'type': 'timespan',
	'timespan': [
		['2019-11-20 00:00:00', '2019-11-20 23:59:59'],
		['2019-11-21 06:00:00', '2019-11-21 09:00:00']
	]
}
```

## 简介
Time-NLP的python3版本   
python 版本https://github.com/sunfiyes/Time-NLPY  
Java 版本https://github.com/shinyke/Time-NLP

## 使用方式 
demo：python3 Test.py

优化说明
    
| 问题          | 以前版本                                     | 现在版本                    |
| ----------- | ---------------------------------------- | ---------------------- |
| 无法解析下下周末     | "timestamp": "2018-04-01 00:00:00"                                    | "timestamp": "2018-04-08 00:00:00"                 |
| 无法解析 3月4         | "2018-03-01"                                   | "2018-03-04"               |
| 无法解析 初一 初二      | cannot parse                                    | "2018-02-16"              |
| 晚上8点到上午10点之间  无法解析上午      | ["2018-03-16 20:00:00", "2018-03-16 22:00:00"] |  ["2018-03-16 20:00:00", "2018-03-16 10:00:00"]|
| 3月21号  错误解析成2019年      | "2019-03-21" | "2018-03-21" |

感谢@[tianyuningmou](https://github.com/tianyuningmou) 目前增加了对24节气的支持


    temp = ['今年春分']
    "timestamp" : "2020-03-20 00:00:00"

## TODO

| 问题          | 现在版本                                     | 正确
| ----------- | ---------------------------------------- | ---------------------- |
| 晚上8点到上午10点之间     |  ["2018-03-16 20:00:00", "2018-03-16 22:00:00"] |  ["2018-03-16 20:00:00", "2018-03-17 10:00:00"]"                                    | "timestamp": "2018-04-08 00:00:00"                 |
