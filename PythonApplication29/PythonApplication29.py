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

        

