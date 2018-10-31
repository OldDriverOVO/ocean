from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# 车型
class CarModels(models.Model):

    id = models.AutoField(primary_key=True)
    cn_name = models.CharField(max_length=128,blank=True)
    en_name = models.CharField(max_length=128)
    img = models.ImageField(upload_to='models/%Y/%m/%d/',blank=True)
    description = models.TextField(blank=True)
    last_change_date = models.DateField()
    last_change_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class META:
        ordering = ['-last_change_date']
    def __str__(self):
        return self.cn_name
# parts
class Parts(models.Model):
    oem = models.CharField(max_length=128,primary_key=True)
    cn_name = models.CharField(max_length=128,blank=True)
    en_name = models.CharField(max_length=128,blank=True)
    img = models.ImageField(upload_to='parts/%Y/%m/%d/',blank=True)
    description = models.TextField(blank=True)
    last_change_date = models.DateTimeField(auto_now=True)
    last_change_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car_model = models.ForeignKey(CarModels,on_delete=models.SET_NULL,null=True)

    class META:
        ordering = ['-last_change_date']

    def __str__(self):
        return self.oem

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128,blank=True)
    nick_name = models.CharField(max_length=128,default='XXXXX')
    description = models.TextField(blank=True)
    icon_img = models.ImageField(upload_to='customer/%Y/%m/%d/', blank=True)
    last_change_date = models.DateTimeField(auto_now=True)
    last_change_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    parts = models.ManyToManyField(Parts,through='CustomerPartsPrice')
    class META:
        ordering = ['-last_change_date']
    def __str__(self):
        return self.name

class CustomerPartsPrice(models.Model):
    id = models.AutoField(primary_key=True)
    oem = models.ForeignKey(Parts, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.FloatField(max_length=11)
    description = models.TextField(blank=True)
    last_change_date = models.DateTimeField(auto_now=True)
    last_change_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class META:
        ordering = ['-last_change_date']
# 工厂
class Factory(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    address= models.CharField(max_length=255,blank=True,default='暂无信息')
    phone_num=models.CharField(max_length=128,blank=True,default='暂无信息')
    qq=models.CharField(max_length=128,blank=True,default='暂无信息')
    Contact = models.CharField(max_length=128,blank=True,default='暂无信息')
    description = models.TextField(blank=True,default='暂无信息')
    last_change_date = models.DateTimeField(auto_now=True)
    last_change_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    parts = models.ManyToManyField(Parts,through='FactoryPartsPrice')
    class META:
        ordering = ['-last_change_date']

    def __str__(self):
        return self.name

class FactoryPartsPrice(models.Model):
    id=models.AutoField(primary_key=True)
    oem = models.ForeignKey(Parts,on_delete=models.CASCADE)
    factory_id =  models.ForeignKey(Factory,on_delete=models.CASCADE)
    price = models.FloatField(max_length=11)
    description = models.TextField(blank=True)
    llast_change_date = models.DateTimeField(auto_now=True)
    last_change_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class META:
        ordering = ['-last_change_date']




class VolumeWeightData(models.Model):
    oem = models.ForeignKey(Parts, on_delete=models.CASCADE)
    num = models.IntegerField(default=1)
    height = models.FloatField(max_length=10,default=0)
    length = models.FloatField(max_length=10,default=0)
    width = models.FloatField(max_length=10,default=0)
    gross_weight = models.FloatField(max_length=10,default=0)
    net_weight = models.FloatField(max_length=10,default=0)
    description = models.TextField(blank=True)
    last_change_date = models.DateTimeField(auto_now=True)
    last_change_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class META:
        ordering = ['last_change_date']

class OemExchange(models.Model):
    ex_oem = models.CharField(max_length=128,primary_key=True)
    oem = models.ForeignKey(Parts, on_delete=models.CASCADE)


    def __str__(self):
        return self.ex_oem


@receiver(pre_delete,sender=Parts)
def part_img_delete(sender, instance, **kwargs):
    instance.img.delete(False)

@receiver(pre_delete,sender=Customer)
def customer_img_delete(sender, instance, **kwargs):
    instance.icon_img.delete(False)