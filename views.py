from platform import uname
import re
import pyttsx3
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.utils.formats import date_format
from django.contrib import messages
from myapp.models import passenger,staff,routes,flights,trip,triptemp,trip_staff,mtemp,booking
import json
from datetime import date
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.db.models import Max, Value
from django.db.models import F
from datetime import datetime,timedelta

# Create your views here.
def index(request):
    rrec=routes.objects.all()
    frec = flights.objects.all()
    trec=trip.objects.all()
    return render(request, 'index.html',{'rrec':rrec,'frec':frec,'trec':trec})
def index2(request):
    rrec = routes.objects.all()
    frec = flights.objects.all()
    trec = trip.objects.all()
    return render(request, 'index.html', {'rrec': rrec, 'frec': frec, 'trec': trec})

def about(request):
    return render(request, 'about.html')
def flightsindex(request):
    frec = flights.objects.all()
    return render(request,'flightsindex.html',{'frec':frec})
def routesindex(request):
    rrec = routes.objects.all()
    return render(request,'routesindex.html',{'rrec':rrec})
def scheduleindex(request):
    trec=trip.objects.all()
    return render(request,'scheduleindex.html',{'trec':trec})
def passreg(request):
    if request.method=="POST":
        pname=request.POST.get('pname')
        emailid = request.POST.get('emailid')
        phoneno = request.POST.get('phoneno')
        place = request.POST.get('place')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        if not re.match(r'^\d{10}$',phoneno):
            msg = "Please..enter..a..valid..phone number..with..10 digits"
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
            return redirect('/pr/')

        rec=passenger.objects.filter(uname=uname,pword=pword)
        if rec:
            msg = "Sorry,this username or password already exists"
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
            return redirect('/pr/')
        else:
            pa=passenger(pname=pname,emailid=emailid,phoneno=phoneno,place=place,age=age,gender=gender,uname=uname,pword=pword)
            pa.save()
            messages.success(request,"Registration successful")
        return redirect('/h/')
    prec=passenger.objects.all()
    return render(request, 'passreg.html',{'prec':prec})
def staffreg(request):
    if request.method=="POST":
        s_name=request.POST.get('s_name')
        emailid = request.POST.get('emailid')
        phoneno = request.POST.get('phoneno')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        s_marital = request.POST.get('s_marital')
        s_qualify = request.POST.get('s_qualify')
        s_exp = request.POST.get('s_exp')
        s_post = request.POST.get('s_post')
        s_photo = request.FILES['s_photo']
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        rec = staff.objects.filter(uname=uname, pword=pword)
        if rec:
            msg = "Sorry,this username or password already exists"
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
            return redirect('/sr/')
        else:
            sa=staff(s_name=s_name,emailid=emailid,phoneno=phoneno,age=age,gender=gender,s_marital=s_marital,s_qualify=s_qualify,s_exp=s_exp,s_post=s_post,s_photo=s_photo,uname=uname,pword=pword)
            sa.save()
        return redirect('/h/')
    srec = staff.objects.all()
    return render(request,'staffreg.html',{'srec':srec})
def adminpage(request):
    return render(request, 'adminpage.html')
def login(request):
    if request.method=="POST":
        uname=request.POST.get('uname')
        pword=request.POST.get('pword')
        found=0
        prec=passenger.objects.filter(uname=uname,pword=pword)
        if prec.exists():
            found=1
            for i in prec:
                id=i.id
                name=i.pname
                rights=i.rights
        if found==0:
            srec=staff.objects.filter(uname=uname,pword=pword)
            if srec.exists():
                found=1
                for j in srec:
                    id=j.id
                    name=j.s_name
                    rights=j.rights
        if found==0:
            msg="Invalid username or password"
            engine=pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
        else:
            request.session['uname']=uname
            request.session['pword'] = pword
            request.session['id'] = id
            request.session['name'] = name
            request.session['rights'] = rights
            if rights=="A":
                return redirect('/a/')
            elif rights=="U":
                return redirect('/u/')
            elif rights=="S":
                return redirect('/s/')
            elif rights=="NS":
                msg = "Sorry, you are not approved yet. Please check again later "
                engine = pyttsx3.init()
                engine.say(msg)
                engine.runAndWait()
            elif rights=="R":
                msg = "Sorry, you are rejected! "
                engine = pyttsx3.init()
                engine.say(msg)
                engine.runAndWait()


    return render(request,'login.html')
def addroutes(request):
    if request.method=="POST":
        rcode = request.POST.get('rcode')
        rname=request.POST.get('rname')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')
        time = request.POST.get('time')
        rec=routes.objects.filter(rname=rname)
        if rec:
            msg = "Sorry...this route already exists "
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
        else:
            ra=routes(rcode=rcode,rname=rname,source=source,destination=destination,distance=distance,time=time)
            ra.save()
    rrec=routes.objects.all()
    return render(request, 'addroutes.html',{'rrec':rrec})
def admineditroutes(request,id):
    if request.method=="POST":
        rcode = request.POST.get('rcode')
        rname=request.POST.get('rname')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')
        time = request.POST.get('time')
        routes.objects.filter(id=id).update(rcode=rcode,rname=rname,source=source,destination=destination,distance=distance,time=time)
        return redirect('/ar/')
    rrec=routes.objects.filter(id=id)
    for j in rrec:
        rcode=j.rcode
        rname=j.rname
        source=j.source
        destination=j.destination
        distance=j.distance
        time=j.time
    return render(request,'admineditroutes.html',{'rcode':rcode,'rname':rname,'source':source,'destination':destination,'distance':distance,'time':time})
def deleteroutes(request,id):
    routes.objects.filter(id=id).delete()
    return redirect('/ar/')
def addflights(request):
    if request.method=="POST":
        fcode = request.POST.get('fcode')
        fname=request.POST.get('fname')
        ftype = request.POST.get('ftype')
        fcapacity= request.POST.get('fcapacity')
        fimage = request.FILES['fimage']
        rec=flights.objects.filter(fcode=fcode)
        if rec:
            msg = "Sorry....this flight already exists "
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
        else:
            fa=flights(fcode=fcode,fname=fname,ftype=ftype,fcapacity=fcapacity,fimage=fimage)
            fa.save()
    frec=flights.objects.all()
    return render(request,'addflights.html',{'frec':frec})
def admineditflights(request,id):
    if request.method=="POST":
        fcode = request.POST.get('fcode')
        fname=request.POST.get('fname')
        ftype = request.POST.get('ftype')
        fcapacity = request.POST.get('fcapacity')
        fluggage= request.POST.get('fluggage')
        flights.objects.filter(id=id).update(fcode=fcode,fname=fname,ftype=ftype,fcapacity=fcapacity,fluggage=fluggage)
        return redirect('/af/')
    frec=flights.objects.filter(id=id)
    for j in frec:
        fcode=j.fcode
        fname=j.fname
        ftype=j.ftype
        fcapacity=j.fcapacity
        fluggage=j.fluggage
    return render(request, 'admineditflights.html', {'fcode': fcode, 'fname': fname, 'ftype': ftype, 'fcapacity':fcapacity,'fluggage':fluggage})

def deleteflights(request,id):
    flights.objects.filter(id=id).delete()
    return redirect('/af/')

def showstafflist(request):
    srec=staff.objects.filter(rights='NS')
    return render(request,'approvestaff.html',{'srec':srec})

def adminapprovestaff(request,id):
    staff.objects.filter(id=id).update(rights='S')
    return redirect("/as/")

def adminrejectstaff(request,id):
    staff.objects.filter(id=id).update(rights='R')
    return redirect("/as/")

def userpage(request):
    return render(request,'userpage.html')


def editstaffprofile(request):
    if request.method=="POST":
        s_name=request.POST.get('s_name')
        emailid = request.POST.get('emailid')
        phoneno = request.POST.get('phoneno')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        s_marital = request.POST.get('s_marital')
        s_qualify = request.POST.get('s_qualify')
        s_exp = request.POST.get('s_exp')
        s_post = request.POST.get('s_post')
        s_photo = request.FILES['s_photo']
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        staff.objects.filter(id=request.session['id']).update(s_name=s_name,emailid=emailid,phoneno=phoneno,age=age,gender=gender,s_marital=s_marital,s_qualify=s_qualify,s_exp=s_exp,s_post=s_post,s_photo=s_photo,uname=uname,pword=pword)
        return redirect('/s/')
    srec = staff.objects.filter(id=request.session['id'])
    for j in srec:
        s_name=j.s_name
        emailid=j.emailid
        phoneno=j.phoneno
        age=j.age,
        gender=j.gender
        s_marital=j.s_marital
        s_qualify=j.s_qualify
        s_exp=j.s_exp
        s_post=j.s_post
        s_photo=j.s_photo
        uname=j.uname
        pword=j.pword
    return render(request, 'editstaffprofile.html',{'s_name':s_name,'emailid':emailid,'phoneno':phoneno,'age':age,'gender':gender,'s_marital':s_marital,'s_qualify':s_qualify,'s_exp':s_exp,'s_post':s_post,'s_photo':s_photo,'uname':uname,'pword':pword})
def edituserprofile(request):
    if request.method == "POST":
        pname = request.POST.get('pname')
        emailid = request.POST.get('emailid')
        phoneno = request.POST.get('phoneno')
        place = request.POST.get('place')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        passenger.objects.filter(id=request.session['id']).update(pname=pname,emailid=emailid,phoneno=phoneno,place=place,age=age,gender=gender,uname=uname,pword=pword)
        return redirect('/u/')
    prec=passenger.objects.filter(id=request.session['id'])
    for j in prec:
        pname = j.pname
        emailid = j.emailid
        phoneno = j.phoneno
        place=j.place
        age = j.age
        gender = j.gender
        uname = j.uname
        pword = j.pword
    return render(request, 'edituserprofile.html',{'pname': pname, 'emailid': emailid, 'phoneno': phoneno, 'place':place, 'age': age, 'gender': gender, 'uname': uname, 'pword': pword})

def admintripschedule0(request):
    if request.method == "POST":
        tdate = request.POST.get('tdate')
        request.session['tdate']=tdate
        return redirect('/ts1/')
    return render(request,'tripschedule0.html')
def admintripschedule1(request):
    rrec=routes.objects.all()
    return render(request,'tripschedule1.html',{'rrec':rrec})
def admintripschedule2(request,id):
    request.session['routeid']=id
    tdate= request.session['tdate']
    trec=trip.objects.filter(tdate=tdate)
    flist=[]
    for j in trec:
        flist.append(j.fcode)

    frec = flights.objects.exclude(id__in=flist)
    return render(request, 'tripschedule2.html', {'frec': frec})
def admintripschedule3(request,id):
    request.session['flightid']=id
    rrec = routes.objects.filter(id=request.session['routeid'])
    frec = flights.objects.filter(id=id)
    tdate = request.session['tdate']
    fdate = date.today()
    max_tno=trip.objects.aggregate(max_tno=Coalesce(Max('tno'), Value(0)))['max_tno']
    tno=int(max_tno)+1
    if request.method == "POST":
        deptime = request.POST.get('deptime')
        arrtime = request.POST.get('arrtime')
        tprice = request.POST.get('tprice')
        request.session['tno']=tno
        request.session['dep']=deptime
        request.session['arr']=arrtime
        request.session['price'] = tprice
        triptemp.objects.all().delete()
        mtemp.objects.all().delete()
        rs=[]
        rec= trip.objects.filter(tdate=tdate)
        for j in rec:
            rs.append(j.tno)
        trec=trip_staff.objects.filter(tcode__in=rs)
        asid=[]
        for j in trec:
            asid.append(j.sid)
        srec=staff.objects.filter(rights='S').exclude(id__in=asid)
        for j in srec:
            ta=triptemp(tcode=0,sid=j.id,s_name=j.s_name,phoneno=j.phoneno,s_post=j.s_post)
            ta.save()
        prec=triptemp.objects.all()

        return render(request, 'tripschedule4.html', {'prec':prec})

    return render(request, 'tripschedule3.html',{'rrec':rrec,'frec':frec,"tno":tno,'fdate':fdate,'tdate':tdate})


def adminfixstaff(request,id):
    rec=triptemp.objects.filter(id=id)
    for j in rec:
        ma=mtemp(tcode=0,sid=j.sid,s_name=j.s_name,phoneno=j.phoneno,s_post=j.s_post)
        ma.save()
    triptemp.objects.filter(id=id).delete()
    prec = triptemp.objects.all()
    mrec = mtemp.objects.all()
    return render(request, 'tripschedule4.html', {'prec':prec,'mrec':mrec})

def admintempdeletestaff(request,id):
    mec=mtemp.objects.filter(id=id)
    for j in mec:
        ta=triptemp(tcode=0,sid=j.sid,s_name=j.s_name,phoneno=j.phoneno,s_post=j.s_post)
        ta.save()
    mtemp.objects.filter(id=id).delete()
    prec = triptemp.objects.all()
    mrec = mtemp.objects.all()
    return render(request, 'tripschedule4.html', {'prec': prec, 'mrec': mrec})

def adminconfirmtrip(request):
   rid=request.session['routeid']
   rec=routes.objects.filter(id=rid)
   for j in rec:
       rname=j.rname
   fid=request.session['flightid']
   flights.objects.filter(id=fid).update(fstatus='Scheduled')

   frec=flights.objects.filter(id=fid)
   for j in frec:
       fname=j.fname
       fcapacity=j.fcapacity
   tr=trip(tno=request.session['tno'],fdate=date.today(),rcode=rid,rname=rname,fcode=fid,fname=fname,deptime=request.session['dep'],arrtime=request.session['arr'],tdate=request.session['tdate'],tprice=request.session['price'],fcapacity=fcapacity,seatremaining=fcapacity,staffstatus='Assigned')
   tr.save()

   mrec=mtemp.objects.all()
   for j in mrec:
       ts=trip_staff(tcode=request.session['tno'],sid=j.sid,s_name=j.s_name,phoneno=j.phoneno,s_post=j.s_post)
       ts.save()
   return redirect('/a/')

def adminviewbooking(request):
    brec=booking.objects.all()
    return render(request,'adminviewbooking.html',{'brec':brec})

def admincanceltrippage(request):
    trec=trip.objects.all()
    return render(request,'admincanceltrip.html',{'trec':trec})
def admindeletetrip(request,tno):
    trip.objects.filter(tno=tno).delete()
    return redirect('/ct/')

def userbooking1(request):
    rrec=routes.objects.all()
    return render(request,'userbooking1.html',{'rrec':rrec})
def userbooking2(request,id):
    request.session['routeid']=id
    tdate=date.today()
    trec = trip.objects.filter(rcode=id,tdate__gte=tdate)
    return render(request, 'userbooking2.html',{'trec':trec})
def userbooking3(request,id):
    request.session['tripid']=id
    trec=trip.objects.filter(id=request.session['tripid'])
    rrec=routes.objects.filter(id=request.session['routeid'])
    bdate = date.today()
    max_bno = booking.objects.aggregate(max_bno=Coalesce(Max('bno'), Value(0)))['max_bno']
    bno = int(max_bno) + 1
    bal=0
    for j in trec:
        bal=j.seatremaining
        price=j.tprice
        rcode=j.rcode
        rname=j.rname
        fcode=j.fcode
        fname=j.fname
        ttime=j.deptime
        tdate=j.tdate
        request.session['tno']=j.tno
    request.session['flightid']=fcode
    frec = flights.objects.filter(id=request.session['flightid'])
    for i in rrec:
        source=i.source
        destination=i.destination
    seats=[]
    for j in range(1,bal+1):
        seats.append(j)
    from datetime import datetime
    data = {"timestamp": tdate}
    json_data = json.dumps(data, default=str)  # Converts datetime to a string
    print(json_data)
    if request.method=="POST":
        pname=request.POST.get('pname')
        passportno=request.POST.get('passportno')
        passportissueplace=request.POST.get('passportissueplace')
        passportexpiry=request.POST.get('passportexpiry')
        nos=request.POST.get('nos')
        total=int(nos)*int(price)
        request.session['rcode']=rcode
        request.session['rname']=rname
        request.session['fcode']=fcode
        request.session['fname']=fname
        request.session['ttime']=ttime
        request.session['source']=source
        request.session['destination']=destination
        request.session['tdate']=json_data
        request.session['bno']=bno
        request.session['pname']=pname
        request.session['passportno']=passportno
        request.session['passportissueplace']=passportissueplace
        request.session['passportexpiry']=passportexpiry
        request.session['nos']=nos
        request.session['price']=price
        request.session['total']=total
        return render(request,'paymentpage.html',{'nos':nos,'price':price,'total':total})
    return render(request, 'userbooking3.html',{'trec':trec,'rrec':rrec,'frec':frec,'bno':bno,'bdate':bdate,'seats':seats})

def confirmbooking(request):
    if request.method=="POST":
        cardno=request.POST.get('cardno')
        nos=request.session['nos']
        trip.objects.filter(id=request.session['tripid']).update(seatfilled=F('seatfilled')+nos,seatremaining=F('seatremaining')-nos)
        ba=booking(bno=request.session['bno'],userid=request.session['id'],tno=request.session['tno'],pname=request.session['pname'],passportno=request.session['passportno'],passportissueplace=request.session['passportissueplace'],passportexpiry=request.session['passportexpiry'],bdate=date.today(),rcode=request.session['rcode'],rname=request.session['rname'],fcode=request.session['fcode'],fname=request.session['fname'],source=request.session['source'],destination=request.session['destination'],tdate=request.session['tdate'],ttime=request.session['ttime'],tprice=request.session['price'],nos=request.session['nos'])
        ba.save()
        return redirect('/u/')
    return render(request,'paymentpage.html')

def cancelbookingpage(request):
    brec=booking.objects.filter(userid=request.session['id'])
    return render(request,'cancelbooking.html',{'brec':brec})

def userdeletebooking(request,bno):
    booking.objects.filter(bno=bno).delete()
    return redirect('/ucb/')

def viewbooking(request):
    brec=booking.objects.filter(userid=request.session['id'])
    return render(request,'viewbooking.html',{'brec':brec})

def staffpage(request):
    return render(request,'staffpage.html')

def staffschedule(request):
    trec=trip.objects.filter(id=request.session['id'])
    return render(request,'staffschedulepage.html',{'trec':trec})

def changep(request):
    if request.method=="POST":
        oldpword=request.POST.get('oldpword')
        newpword=request.POST.get('newpword')
        confirmpword=request.POST.get('confirmpword')
        u=request.session['uname']
        p=request.session['pword']
        if p==oldpword:
            if newpword==confirmpword:
                staff.objects.filter(uname=u,pword=p).update(pword=confirmpword)
                msg = "Password changed successfully"
                engine = pyttsx3.init()
                engine.say(msg)
                engine.runAndWait()
                return redirect('/a/')
    return render(request,"adminchangepassword.html")


def form(request):
    return render(request,'form.html')


