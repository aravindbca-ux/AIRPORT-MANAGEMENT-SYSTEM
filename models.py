from django.db import models
from datetime import date
# Create your models here.
class passenger(models.Model):
    pname=models.CharField(max_length=100)
    emailid=models.EmailField()
    phoneno=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=100)
    uname=models.CharField(max_length=100)
    pword=models.CharField(max_length=100)
    rights=models.CharField(default='U',max_length=100)

class staff(models.Model):
    s_name=models.CharField(max_length=100)
    emailid=models.EmailField()
    phoneno=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=100)
    s_marital=models.CharField(max_length=100)
    s_qualify=models.CharField(max_length=100)
    s_exp=models.CharField(max_length=100)
    s_post=models.CharField(max_length=100)
    s_photo=models.ImageField(upload_to='photos/')
    uname=models.CharField(max_length=100)
    pword=models.CharField(max_length=100)
    work_status=models.CharField(default='F',max_length=100)
    rights=models.CharField(default='NS' ,max_length=100)

class routes(models.Model):
    rcode=models.CharField(max_length=100)
    rname=models.CharField(max_length=100)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    distance=models.CharField(max_length=100)
    time=models.CharField(max_length=100)

class flights(models.Model):
    fcode=models.CharField(max_length=100)
    fname=models.CharField(max_length=100)
    ftype=models.CharField(max_length=100)
    fcapacity=models.IntegerField()
    fluggage=models.IntegerField(default='20')
    fimage=models.ImageField(upload_to='photos/')
    fstatus=models.CharField(default='f',max_length=100)

class trip(models.Model):
    tno=models.IntegerField()
    fdate = models.DateField()
    rcode=models.CharField(max_length=100)
    rname=models.CharField(max_length=100)
    fcode=models.CharField(max_length=100)
    fname=models.CharField(max_length=100)
    deptime=models.CharField(max_length=100)
    arrtime=models.CharField(max_length=100)
    tdate=models.DateField()
    tprice=models.FloatField()
    fcapacity=models.CharField(max_length=100)
    seatfilled=models.IntegerField(default=0)
    seatremaining=models.IntegerField(default=0)
    staffstatus=models.CharField(default='Not Assigned',max_length=100)
    tripstatus=models.CharField(default="F",max_length=100)

class trip_staff(models.Model):
    tcode=models.CharField(max_length=100)
    sid=models.IntegerField(default=0)
    s_name=models.CharField(max_length=100)
    phoneno=models.CharField(max_length=100)
    s_post=models.CharField(max_length=100)

class triptemp(models.Model):
    tcode=models.CharField(max_length=100)
    sid = models.IntegerField(default=0)
    s_name=models.CharField(max_length=100)
    phoneno=models.CharField(max_length=100)
    s_post=models.CharField(max_length=100)

class mtemp(models.Model):
    tcode=models.CharField(max_length=100)
    sid = models.IntegerField(default=0)
    s_name=models.CharField(max_length=100)
    phoneno=models.CharField(max_length=100)
    s_post=models.CharField(max_length=100)

class booking(models.Model):
    bno=models.IntegerField()
    userid=models.IntegerField(default=0)
    tno=models.IntegerField()
    pname=models.CharField(max_length=100)
    passportno=models.CharField(max_length=100)
    passportissueplace=models.CharField(max_length=100)
    passportexpiry=models.DateField()
    bdate=models.CharField(max_length=100)
    rcode=models.CharField(max_length=100)
    rname=models.CharField(max_length=100)
    fcode=models.CharField(max_length=100)
    fname=models.CharField(max_length=100)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    tdate=models.CharField(max_length=100)
    ttime=models.CharField(max_length=100,default='x')
    tprice=models.FloatField()
    nos=models.IntegerField(default=0)

