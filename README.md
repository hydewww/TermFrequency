# 词频分析

为摆脱无脑谷歌翻译而诞生的程序，希望能帮助自己啃下绝望的众英文文档。

## 用法

### Main.py

0. 输出文件夹为**output**

1. 读取**text**文件夹中文档(utf-8)，统计词频并排序，筛选某比例内(50%-70%)的词汇，输出至**all.csv**

2. 读取**buildin_dicts**文件夹中字典(现为六级词汇)，筛选出1中有的单词并添加释义，输出**found.csv** **notfound.csv**

- 代码末尾有可改变的参数

### GenerateDicts.py

- 需修改分词部分的代码

- 将新词典放至**new_dicts**，运行后会在**buildin_dicts**生成Main.py所需格式的词典

## Todo

- 网络查词