from django.db import models

class Members(models.Model):
    table_id = models.IntegerField(default=1)
    x1 = models.FloatField()
    x2 = models.FloatField()
    y = models.FloatField()

class Members_3(models.Model):
    table_id = models.IntegerField(default=1)
    x1 = models.FloatField()
    x2 = models.FloatField()
    x3 = models.FloatField()
    y = models.FloatField()

class Members_4(models.Model):
    table_id = models.IntegerField(default=1)
    x1 = models.FloatField()
    x2 = models.FloatField()
    x3 = models.FloatField()
    x4 = models.FloatField()
    y = models.FloatField()

class Members_5(models.Model):
    table_id = models.IntegerField(default=1)
    x1 = models.FloatField()
    x2 = models.FloatField()
    x3 = models.FloatField()
    x4 = models.FloatField()
    x5 = models.FloatField()
    y = models.FloatField()


class Members_6(models.Model):
    table_id = models.IntegerField(default=1)
    x1 = models.FloatField()
    x2 = models.FloatField()
    x3 = models.FloatField()
    x4 = models.FloatField()
    x5 = models.FloatField()
    x6 = models.FloatField()
    y = models.FloatField()


class user_table(models.Model):
    user_id = models.IntegerField(default=1)
    feature = models.IntegerField(default=2)
    table_id = models.IntegerField(default=1)
    table_name = models.CharField(max_length=200,default="")
    

class history(models.Model):
    ID = models.AutoField(primary_key=True)
    loss = models.FloatField()
    epoch = models.CharField(max_length=200)
    lr = models.CharField(max_length=200)
    layers = models.CharField(max_length=200)
    table_id = models.IntegerField(default=1)