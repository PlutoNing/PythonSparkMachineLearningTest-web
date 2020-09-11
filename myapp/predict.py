from __future__ import print_function

from pyspark import SparkConf, SparkContext
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
from pyspark.mllib.evaluation import BinaryClassificationMetrics
from myapp.views import *
import os
import time

os.environ['PYSPARK_PYTHON'] =PYTHON_PATH

'''
global vars

'''



def isunfit(lp):
    a, b = lp[0], lp[1]
    if a - 0 >= 0.1:
        a = 1
    if b - 0 >= 0.1:
        b = 1

    if a - b <= 0.1:
        return False
    else:
        return True


def tobin(num):
    if num - 0 >= 0.1:
        num = 1.0
    else:
        num = 0.0
    return num


def parse_label(label):
    labels = {0: 'Benign',
              1: 'Brute Force -Web',
              2: 'Bot',
              3: 'FTP-BruteForce',
              4: 'DoS attacks-SlowHTTPTest',
              5: 'DDOS attack-HOIC',
              6: 'DDOS attack-LOIC-UDP',
              7: 'Infilteration',
              8: 'DoS attacks-Slowloris',
              9: 'DoS attacks-Hulk',
              10: 'DoS attacks-GoldenEye',
              11: 'SSH-Bruteforce',
              12: 'Brute Force -XSS',
              13: 'SQL Injection'
              }

    return str(labels[label])


def analyse_result(predict_list):
    label_nums = len(predict_list)
    numberOfEachSort = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for predict_label in predict_list:
        label = int(predict_label)
        numberOfEachSort[label] = numberOfEachSort[label] + 1
    rateOfEachSort = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # for i ,num in zip(range(13),rateOfEachSort) :

    rateOFsort_dict = {
        'Benign': 0,
        'Brute Force -Web': 0,
        'Bot': 0,
        'FTP-BruteForce': 0,
        'DoS attacks-SlowHTTPTest': 0,
        'DDOS attack-HOIC': 0,
        'DDOS attack-LOIC-UDP': 0,
        'Infilteration': 0,
        'DoS attacks-Slowloris': 0,
        'DoS attacks-Hulk': 0,
        'DoS attacks-GoldenEye': 0,
        'SSH-Bruteforce': 0,
        'Brute Force -XSS': 0,
        'SQL Injection': 0
    }

    for i in range(14):
        rateOFsort_dict[parse_label(i)] = numberOfEachSort[i] / label_nums

    return rateOFsort_dict


def save(predictlabel_list):
    with open('result.txt', 'w') as f:
        filelist = os.listdir(DATA_PATH)
        for filename in filelist:
            filepath = DATA_PATH + "\\" + filename
            with open(filepath, 'r') as r:

                for label, line in zip(predictlabel_list, r.readlines()):
                    line = ' '.join(line.split(' ').pop(0))
                    line = line.replace(' ', '')
                    new_line = str(label) + "-->" + line + "\n"
                    f.write(new_line)


def predict():
    conf = SparkConf().setMaster("local").setAppName("My App")
    sc = SparkContext(conf=conf)

    testData = MLUtils.loadLibSVMFile(sc, TEST_DATA_PATH)

    model = RandomForestModel.load(sc, TEST_MODEL_PATH)

    predictions = model.predict(testData.map(lambda x: x.features))

    predictlabel_list = predictions.collect()

    rateOFeachSort_dict = analyse_result(predictlabel_list)

    save(predictlabel_list)

    return rateOFeachSort_dict
