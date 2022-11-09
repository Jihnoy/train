# -*- coding: utf-8 -*-
# 生成文件夹中所有文件的路径到txt
import os


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        list_name.append(file)


list_name = []
path = '../dataset/images/train/'  # 文件夹路径
listdir(path, list_name)
print(list_name)

with open('../dataset/train_list.txt', 'w') as f:  # 要存入的txt
    write = ''
    for i in list_name:
        write = 'dataset/images/train/' + str(i) + '\n'
        f.write(write)


