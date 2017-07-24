# -*- coding: utf-8 -*-

import codecs
import os

# 1.获取文件路径列表
def get_file_from_folder(folder_path):
  paths = []
  for root, dirs, files in os.walk(folder_path): # .walk()遍历文件夹
    for file in files:
      file_path = os.path.join(root, file) # path.join 将目录和文件名组合成路径
      paths.append(file_path)
  print ("总共",len(paths),"个文件")
  return paths

# 3.分词
## 3.1去除非英文字符
def format_word(text):
    fmt = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '  # 注意空格
    for char in text:
        if char not in fmt:
            text = text.replace(char, ' ')       # 用' '替换文本中的char
    return text.lower()     # Todo: 解决JAVA等大写问题

## 3.2处理单字母
def discard_single(words):
    new_words = []
    for word in words:
        if len(word) > 1:
            new_words.append(word)
    return new_words

## 3.0  text由文件操作传递
def process_words(text):
    text = format_word(text)
    words = text.split(' ')
    words = discard_single(words)
    return words

# 2.文件操作
## 2.2读取单文件 返回单词
def read_file(file_path):
  words = []
  f = codecs.open(file_path, 'r', "utf-8")
  lines = f.readlines()   # .readlines()返回各行组成的list
  for line in lines:
    line = line.strip()   # .strip() 清除行尾'\n'
    if len(line) > 0:     # 本行非空
        words.extend(process_words(line))
  return words

## 2.1读取所有文件 整合所有单词
def read_files(paths):
    world_words = []
    for index,path in enumerate(paths):
        words = read_file(path)
        world_words.extend(words)
    print ("分词over")
    return world_words

# 4.统计词频
def statictics_words(words):
  s_dict = {}
  for word in words:
    if word in s_dict:
      s_dict[word] = s_dict[word] + 1
    else:
      s_dict[word] = 1
  return s_dict

# 5.排序
def sort_by_value(word_dict):
  items = word_dict.items()     # 返回(key,value)的list
  item_list = [[it[1], it[0]] for it in items]  # key,value换位
  item_list.sort(reverse=True)  # reverse降序排序
  return item_list

# 6.百分比统计
def rate_statistics(items_list,total_num,rate_on):
    rate_begin,rate_end = 0, 100
    if rate_on:
        rate_begin , rate_end = rate[0],rate[1]
    final_list = []
    curr_total = 0
    for item in items_list:
        curr_total = curr_total + item[0]
        curr_percent = (float(curr_total) / total_num) * 100
        if curr_percent<rate_begin:
            continue
        if curr_percent>rate_end:
            break
        curr_percent_str = '%0.3f' % (curr_percent)
        final_list.append([item[1],str(item[0]),curr_percent_str,''])  # 单词-词频-百分比
    print ('排序over')
    return final_list

# 7.添加释义    # Todo:网络查词
## 7.1读取词典
def read_dict(dict_path):
    dicts = {}
    f = codecs.open(dict_path, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        list = line.split("_____", 1)
        word = list[0]
        value = list[1]
        dicts[word] = value
    print("已获取", len(dicts.keys()), '个单词释义')
    return dicts

# 7.2 添加释义
def add_meaning(final_list,dicts):
    found_words = []
    notfound_words = []
    for item in final_list:
        word = item[0]
        if word in dicts.keys():
            item[3]=dicts[word]
            found_words.append(item)
        else:
            notfound_words.append(item)
    return found_words,notfound_words

# 8.输出csv
def print_to_csv(word_list, to_file_path):
    nfile = open(to_file_path,'w+')
    if show_statistics:
        for item in word_list:
            nfile.write("%s,%s,%s,%s\n" % (item[0], item[1],item[2],item[3]))
    else :
        for item in word_list:
            nfile.write("%s,%s\n" % (item[0], item[3]))
    nfile.close()
    print ("输出文件",to_file_path)

def main():
    # words = read_file('data1/dt01.txt')
    file_path = get_file_from_folder('text') #1.获取文件路径列表

    words = read_files(file_path) #2.3.读取文件并分词

    total_num = len(words)
    word_dict = statictics_words(words)   #4.统计词频

    word_list = sort_by_value(word_dict) #5.排序

    word_list = rate_statistics(word_list,total_num, rate_on)  #6.百分比统计  True-按百分比
    print_to_csv(word_list, 'output\\all.csv')

    dict_path = get_file_from_folder('buildin_dicts')   # Todo:改成多字典
    dicts = read_dict(dict_path[0])    #7.1读取词典
    found_words, notfound_words = add_meaning(word_list,dicts) # 7.2 生成单词释义

    print_to_csv(found_words, 'output\\found.csv')
    print_to_csv(notfound_words, 'output\\notfound.csv') # 8.输出至文档


if __name__ == "__main__":
    # 将需修改的参数放至此处 方便修改
    rate_on = False  # 筛选百分比开关
    rate = [40,70]  # 百分比始末
    show_statistics = True  # 显示词频&百分比
    eachday_recite_num = 20 # 每天背单词数
    main()
