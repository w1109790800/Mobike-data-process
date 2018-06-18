---
layout: mobike
title: mobike爬虫数据分析
date: 2018-02-22 14:12:21
tags:
---
# Mobike 爬虫数据分析


---

在上次爬虫的文章之后，这几天又积累了很多数据。如下图
![](http://blogphotos.oss-cn-beijing.aliyuncs.com/2018/454bfc3f2c739229f3e27aaa1f07790.png)
![](http://blogphotos.oss-cn-beijing.aliyuncs.com/2018/96fac9bc5f9857893e121bbafa67666.png)
于是准备着手分析这些GPS数据
##数据格式

如下：
![](http://blogphotos.oss-cn-beijing.aliyuncs.com/2018/ad2984ab0993920c466114e3f627b0c.png)

即第一列为 ： ID
第二列：X（经度）
第三列：Y（维度）

在这些信息的基础上，我们分析 需要去除 和需要留下的数据进行数据筛选。
在没有筛选之前，用arcGIS画出来基本就是一个大黑疙瘩，，，

##数据筛选

需要留下：
```
id相等的位置不同的车
```
需要去除：
```
id不想等的车
位置变化过大的车
位置变化极小的车
```

明确目标后 使用`python`编写程序 如下：
其中有一个函数非常好用，可以将str类型的数据转换为float类型
这里也一起放出来：
```python
def fileload(filename):
    csvfile = open(filename, encoding = 'utf-8')
    data = csv.reader(csvfile)
    dataset = []
    for line in data:
        dataset.append(line)
    csvfile.close()
    return dataset
def str2float(s):
  return reduce(lambda x,y:x+int2dec(y),map(str2int,s.split('.')))
def char2num(s):
  return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
def str2int(s):
  return reduce(lambda x,y:x*10+y,map(char2num,s))
def intLen(i):
  return len('%d'%i)
def int2dec(i):
  return i/(10**intLen(i))

```
使用时仅需要调用 `str2float(s)`即可 返回值即为float类型
下面是筛选程序
```python 
for temline1 in range(1,line1):
    for temline2 in range(1,line2):
        if file1[temline1][id] == file2[temline2][id]:
          if (file1[temline1][x] != file2[temline2][x] ) and (file1[temline1][y] != file2[temline2][y] ):
            #print(file1[temline1][x])
            #print(file2[temline2][x])
            subx = abs(str2float(str(file1[temline1][x])) - str2float(str(file2[temline2][x])))
            suby = abs(str2float(str(file1[temline1][y])) - str2float(str(file2[temline2][y])))
            #print(str(subx) + str(suby))
            #print(temline2)
            if (subx > 0.0001 ) and (suby > 0.0001):

                if (subx < 0.4) and (suby < 0.4 ):
                    print('subX : ' + str(subx))
                    print('subY : ' + str(suby))
                    print(file1[temline1])
                    print(file2[temline2])
                    csv_writer = csv.writer(out)
                    csv_writer.writerow([file1[temline1][0],file1[temline1][1],file1[temline1][2] , " * " , file2[temline2][0],file2[temline2][1],file2[temline2][2]] )
                    break
```
这一段就是专门用来去除不符合条件的车辆
两个`for`循环用于遍历两个文件
内层循环中的多个`if`分别保留下了符合条件的数据

这样数据就可以被arcgis读取并转化为线。

##完整程序

```python
import csv
import csv
import os
import time
import math
from functools import reduce
n1 = '2018-02-22,04-10-40.csv'
n2 = '2018-02-22,09-50-45.csv'
def fileload(filename):
    csvfile = open(filename, encoding = 'utf-8')
    data = csv.reader(csvfile)
    dataset = []
    for line in data:
        dataset.append(line)
    csvfile.close()
    return dataset
def str2float(s):
  return reduce(lambda x,y:x+int2dec(y),map(str2int,s.split('.')))
def char2num(s):
  return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
def str2int(s):
  return reduce(lambda x,y:x*10+y,map(char2num,s))
def intLen(i):
  return len('%d'%i)
def int2dec(i):
  return i/(10**intLen(i))
temp = 0  
id = 0
x = 1
y = 2
file1=fileload(n1)
file2=fileload(n2)
out = open('output.csv', 'w')
line1 = len(file1)
line2 = len(file2)
for temline1 in range(1,line1):
    for temline2 in range(1,line2):
        if file1[temline1][id] == file2[temline2][id]:
          if (file1[temline1][x] != file2[temline2][x] ) and (file1[temline1][y] != file2[temline2][y] ):
            #print(file1[temline1][x])
            #print(file2[temline2][x])
            subx = abs(str2float(str(file1[temline1][x])) - str2float(str(file2[temline2][x])))
            suby = abs(str2float(str(file1[temline1][y])) - str2float(str(file2[temline2][y])))
            #print(str(subx) + str(suby))
            #print(temline2)
            if (subx > 0.0001 ) and (suby > 0.0001):

                if (subx < 0.4) and (suby < 0.4 ):
                    print('subX : ' + str(subx))
                    print('subY : ' + str(suby))
                    print(file1[temline1])
                    print(file2[temline2])
                    csv_writer = csv.writer(out)
                    csv_writer.writerow([file1[temline1][0],file1[temline1][1],file1[temline1][2] , " * " , file2[temline2][0],file2[temline2][1],file2[temline2][2]] )
                    break

os.rename('output.csv', n1 + "-"  + n2 + ".csv")
```

这里还有几个小问题：
经纬度控制的最佳数值还没有找到，这个还需要改一改。
此外，筛选程序效率低 速度比较慢

GIS截图：
![](http://blogphotos.oss-cn-beijing.aliyuncs.com/2018/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE3.png)
![](http://blogphotos.oss-cn-beijing.aliyuncs.com/2018/mobike-gis/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE12.png)
![](http://blogphotos.oss-cn-beijing.aliyuncs.com/2018/mobike-gis/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE10.png)
#未完待续 ……