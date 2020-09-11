import os
import shutil
from myapp.models import Pac
from django.http import HttpResponse


def del_file(filepath):
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def clear_model():
    if Pac.objects.all().exists():
        Pac.objects.all().delete()


def test():
    if Pac.objects.all().exists():
        Pac.objects.all().delete()
    return HttpResponse("ok")


def parse_label(label):
    labels = {'Benign': 0,
              'Brute Force -Web': 1,
              'Bot': 2,
              'FTP-BruteForce': 3,
              'DoS attacks-SlowHTTPTest': 4,
              'DDOS attack-HOIC': 5,
              'DDOS attack-LOIC-UDP': 6,
              'Infilteration': 7,
              'DoS attacks-Slowloris': 8,
              'DoS attacks-Hulk': 9,
              'DoS attacks-GoldenEye': 10,
              'SSH-Bruteforce': 11,
              'Brute Force -XSS': 12,
              'SQL Injection': 13
              }

    return str(labels[label])


def construct_line(label, line):
    new_line = []

    try:
        if float(label) == 0.0:
            label = "0"
    except ValueError:
        pass

    new_line.append(label)

    for i, item in enumerate(line):

        # convert TimeString to TimeStamp
        try:
            if item == '' or float(item) == 0.0:
                continue
        except ValueError:
            import time
            timeArray = time.strptime(item, "%m/%d/%Y %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            item = timeStamp

        new_item = "%s:%s" % (i + 1, item)
        new_line.append(new_item)
    new_line = " ".join(new_line)
    new_line += "\n"
    return new_line
