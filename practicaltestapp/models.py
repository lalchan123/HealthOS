from ensurepip import bootstrap
from enum import unique
from django.db import models

# Create your models here.

class PlansModel(models.Model):
    plan_name = models.CharField(max_length=250)
    per_month_pay_bd_taka = models.IntegerField()
    durability = models.IntegerField()
    dial_number = models.CharField(max_length=250)
    plan_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.plan_name
    
COLOR_CHOICES = (
    ('GP','GP'),
    ('Robi', 'Robi'),
    ('Banglalink','Banglalink'),
    ('Airtel','Airtel'),
)    

class Customer(models.Model):
    first_name = models.CharField(max_length=250) 
    last_name = models.CharField(max_length=50) 
    phone_number=  models.CharField(max_length=15, unique=True) 
    nid = models.CharField(max_length=150)
    company_operator = models.CharField(max_length=50, choices=COLOR_CHOICES, default='GP')
    
    def __str__(self):
        return self.phone_number
    
    
    
class PlanCustomerBuyPay(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plans_offer = models.ForeignKey(PlansModel, on_delete=models.CASCADE)
    per_month_pay_bd_amount= models.IntegerField()
    plan_active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    offer_activation_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.customer.first_name} {self.customer.phone_number} {self.plans_offer.plan_name}'
    