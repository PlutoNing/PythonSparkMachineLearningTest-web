from myapp.models import Pac
import os
import csv, time
from itertools import islice
from myapp.utils import *
import sys


def csvProcess():
    csvDir = r'C:\\Users\pluto\PycharmProjects\djangoProject\CsvDir\\'
    csvtomodel()
    csvtolibsvm()
    del_file(csvDir)


def csvtomodel():
    flag = -1
    csvDir = r'C:\\Users\pluto\PycharmProjects\djangoProject\CsvDir\\'
    clear_model()
    file_list = os.listdir(csvDir)

    for filename in file_list:
        filepath = csvDir + filename
        with open(filepath) as f:
            lines = f.readlines()[1:]
            for line in lines:
                list = line.split(',')
                if len(list) > 7:
                    if str(list[2]).isdigit():
                        tmpPac = Pac(time=list[6], srcIP=list[1], srcPort=int(list[2]), dstIP=list[3],
                                     dstPort=(list[4]), \
                                     protocol=list[5], length=(list[2]), info=list[0])
                        # 这里的length找不到是哪个字段 ，所以先随便填了一个，
                        tmpPac.save()
                    else:
                        continue


def csvtolibsvm():
    csvDir = r'C:\\Users\pluto\PycharmProjects\djangoProject\CsvDir\\'
    libsvmDir = r'C:\\Users\pluto\PycharmProjects\djangoProject\libsvm\\'

    file_list = os.listdir(csvDir)

    for filename in file_list:
        filepath = csvDir + filename
        filename_list = filename.split('.')
        filename_list.pop()
        ofilename = '.'.join(filename_list)
        i = open(filepath, 'r')
        output_file = libsvmDir + ofilename + '.libsvm'
        o = open(output_file, 'w')
        # o.write("hello")
        reader = csv.reader(i)
        for line in reader:
            if str(line[2]).isdigit():
                line.pop(0)
                line.pop(0)
                line.pop(0)
                line.pop(0)
                line.pop()
                label = '-100'
                date = str(line[2])
                time_list = date.split(' ')
                time_list.pop()
                atime = ' '.join(time_list)

                timeArray = time.strptime(atime, "%m/%d/%Y %H:%M:%S")
                timeStamp = int(time.mktime(timeArray))
                line[2] = timeStamp
                new_line = construct_line(label, line)

                o.write(new_line)
            else:
                continue


def construct_line(label, line):
    new_line = []

    try:
        if float(label) == 0.0:
            label = "0"
    except ValueError:
        pass

    new_line.append(label)

    for i, item in enumerate(line):
        new_item = "%s:%s" % (i + 1, item)
        new_line.append(new_item)
    new_line = " ".join(new_line)
    new_line += "\n"
    return new_line
