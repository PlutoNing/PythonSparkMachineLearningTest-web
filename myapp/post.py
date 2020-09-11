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
from myapp.models import Pac
from myapp.pcap2csv import pcap2csv
from myapp.csvProcess import *
from myapp.predict import predict
from myapp.utils import clear_model




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

    contacts=getEmptyPack()
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
    libsvmDir = r"C:\Users\pluto\PycharmProjects\djangoProject\libsvm\\"
    csvDir = r"C:\Users\pluto\PycharmProjects\djangoProject\CsvDir\\"
    pcapDir = r"C:\Users\pluto\PycharmProjects\djangoProject\uploads\\"
    del_file(libsvmDir)
    del_file(csvDir)
    del_file(pcapDir)
    clear_model()
