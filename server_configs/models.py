from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class WorklistConfigs(models.Model):
    worklist_ae = models.CharField(max_length=20)
    worklist_ip = models.CharField(max_length=30)
    worklist_port = models.IntegerField(MinValueValidator(0))


class DestinationConfigs(models.Model):
    destination_ae = models.CharField(max_length=20)
    destination_ip = models.CharField(max_length=30)
    destination_port = models.IntegerField(MinValueValidator(0))
