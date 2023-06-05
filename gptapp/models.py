from django.db import models

# Create your models here.
#/project1/gptapp/model.py
class genip_db(models.Model):
    username = models.CharField(max_length=255)
    input = models.CharField(max_length=100000)
    language = models.CharField(max_length=255)
    output_1st = models.CharField(max_length=500000)
    duration1 = models.FloatField()
    output_2nd = models.CharField(max_length=500000)
    duration2 = models.FloatField()
    rate = models.IntegerField(default=0)
    timestamp = models.DateTimeField('Time Stamp')
    ip = models.CharField(max_length=30)
    temperature = models.FloatField()
    free = models.IntegerField(default=0)

    def __str__(self):
        return self.input

class freecount(models.Model):
    username = models.CharField(max_length=255)
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.output