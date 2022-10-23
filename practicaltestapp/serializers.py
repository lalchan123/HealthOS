from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from practicaltestapp.models import *



class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        

class PlanCustomerBuyPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanCustomerBuyPay
        fields = '__all__'        