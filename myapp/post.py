# pylint: disable=no-member
import os, math
from datetime import datetime
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
# from .models import myPost, myUser, tmpPost
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .mylib import myrender, myrenderw
from django.conf import settings
from myapp.models import Pac

from myapp.pcap2csv import pcap2csv
from myapp.csvProcess import *
from myapp.predict import predict
from myapp.utils import clear_model
from myapp.views import *


def post(request):
    clear_env()

    packs = getEmptyPack()
    dict = getEmptyDict()

    ctx = {
        "packs": packs,
        "dict": dict,
    }

    HttpResponse = render(request, 'off-line.html', ctx)
    return HttpResponse


def getpost(request):
    global result_dict

    contacts = getEmptyPack()
    if 'page' not in request.GET:
        if 'upload' in request.FILES:
            f = request.FILES.get('upload')
            astr = f.name

            filename = os.path.join(settings.MEDIA_ROOT, f.name)

            des = open(filename, 'wb+')
            for chunk in f.chunks():
                des.write(chunk)
            des.close()  # pcap文件上传成功

            pcap2csv()  # 转换为csv并删除这个pcap文件

            csvProcess()  # 这里把csv转到数据库和libsvm
            result_dict = predict()  # 这里分析每种攻击类型的比率
            save_result(result_dict)
            packs = Pac.objects.all()
            paginator = Paginator(packs, 10)
            list = request.GET.get('page')
            try:
                contacts = paginator.page(list)
            except PageNotAnInteger:
                contacts = paginator.page(1)

            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
    else:
        packs = Pac.objects.all()
        result_dict=get_result()
        paginator = Paginator(packs, 10)
        list = request.GET.get('page')
        try:
            contacts = paginator.page(list)
        except PageNotAnInteger:
            contacts = paginator.page(1)

        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

    ctx = {
        "packs": contacts,
        "dict": result_dict,
    }

    HttpResponse = render(request, 'off-line.html', ctx)
    return HttpResponse


def getEmptyPack():
    pack = Pac(time="no data", srcIP="no data", srcPort=0, dstIP="no data", dstPort=0, \
               protocol="no data", length=0, info="no data")
    packs = [pack]

    return packs


def getEmptyDict():
    return {
        'Benign': 'no data',
        'Brute Force -Web': 'no data',
        'Bot': 'no data',
        'FTP-BruteForce': 'no data',
        'DoS attacks-SlowHTTPTest': 'no data',
        'DDOS attack-HOIC': 'no data',
        'DDOS attack-LOIC-UDP': 'no data',
        'Infilteration': 'no data',
        'DoS attacks-Slowloris': 'no data',
        'DoS attacks-Hulk': 'no data',
        'DoS attacks-GoldenEye': 'no data',
        'SSH-Bruteforce': 'no data',
        'Brute Force -XSS': 'no data',
        'SQL Injection': 'no data'
    }


def clear_env():
    del_file(LIBSVM_DiR)
    del_file(CSV_DIR)
    del_file(PCAP_DIR)
    clear_model()


def vis(request):
    return render(request, 'visualize.html')


def index(request):
    HttpResponse = render(request, 'index.html')
    return HttpResponse

def get_result():
    dict = {
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


    with open('dict.txt','r') as f:

        lines = f.readlines()
        for key,line in zip(dict,lines):
            dict[key] = line
    return dict



def save_result(dict):
    with open('dict.txt', 'w') as f:
        for key, value in dict.items():
            f.write(str(value))
            f.write('\n')


