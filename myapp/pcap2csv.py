import os
from myapp.utils import *
from myapp.views import *


def pcap2csv():  # 把用户上传的pcap包转成csv
    command = " java {} -jar {}  {} {}".format(VM_OPTIONS, JAR_PATH, PCAP_DIR, CSV_DIR)
    os.system(command)
    del_file(PCAP_DIR)
