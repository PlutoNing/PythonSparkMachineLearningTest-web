from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Pac(models.Model):
    id = models.AutoField(primary_key=True)
    pcapname = models.CharField(max_length=100, default="pcap")
    time = models.CharField(max_length=100)
    srcIP = models.CharField(max_length=50)
    srcPort = models.IntegerField()
    dstIP = models.CharField(max_length=50)
    dstPort = models.IntegerField()
    protocol = models.CharField(max_length=30)
    length = models.IntegerField()
    info = models.TextField(max_length=300)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['time']
