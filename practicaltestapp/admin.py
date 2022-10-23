from django.contrib import admin

from practicaltestapp.models import *

# Register your models here.

admin.site.register(PlansModel)
admin.site.register(Customer)
admin.site.register(PlanCustomerBuyPay)