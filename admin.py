from django.contrib import admin
from myapp.models import passenger,staff,routes,flights,trip,trip_staff,triptemp,booking

# Register your models here.
class passengerAdmin(admin.ModelAdmin):
    list_display = ('id','pname','emailid','phoneno','place','age','gender','uname','pword','rights')
admin.site.register(passenger,passengerAdmin)

class staffAdmin(admin.ModelAdmin):
    list_display = ('id','s_name','emailid','phoneno','age','gender','s_marital','s_qualify','s_exp','s_post','s_photo','uname','pword','work_status','rights')
admin.site.register(staff,staffAdmin)

class routesAdmin(admin.ModelAdmin):
    list_display = ('id','rcode','rname','source','destination','distance','time')
admin.site.register(routes,routesAdmin)

class flightsAdmin(admin.ModelAdmin):
    list_display = ('id','fcode','fname','ftype','fcapacity','fluggage','fimage','fstatus')
admin.site.register(flights,flightsAdmin)

class tripAdmin(admin.ModelAdmin):
    list_display = ('id','tno','fdate','rcode','rname','fcode','fname','deptime','arrtime','tdate','tprice','fcapacity','seatfilled','seatremaining','staffstatus')
admin.site.register(trip,tripAdmin)

class trip_staffAdmin(admin.ModelAdmin):
    list_display = ('id','tcode','sid','s_name','phoneno','s_post')
admin.site.register(trip_staff,trip_staffAdmin)

class triptempAdmin(admin.ModelAdmin):
    list_display = ('id','tcode','sid','s_name','phoneno','s_post')
admin.site.register(triptemp,triptempAdmin)

class bookingAdmin(admin.ModelAdmin):
    list_display = ('bno','tno','pname','passportno','passportissueplace','passportexpiry','bdate','rcode','rname','fcode','fname','source','destination','tdate','ttime','tprice','nos')
admin.site.register(booking,bookingAdmin)