from django.shortcuts import render, redirect
from datetime import datetime
# import datetime
# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response


from practicaltestapp.serializers import *

from practicaltestapp.models import *


# ssl commerce
from sslcommerz_lib import SSLCOMMERZ

# Create your views here.


## for customer registration view start
@api_view(['POST'])
def CustomerRegistration(request):
    try:
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        phone_number = request.data['phone_number']
        nid = request.data['nid']
        company_operator = request.data['company_operator']
        
        val_mobile = validateMobile(phone_number)
        if val_mobile==False:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Mobile Number is not valid!"}, status=status.HTTP_400_BAD_REQUEST)
        if Customer.objects.filter(phone_number=phone_number).exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Phone number already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        
        customer = Customer.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number, nid=nid, company_operator=company_operator)
        customer.save()
        
        customer_serializer = CustomerRegistrationSerializer(customer, many=False)
        return Response({'status':status.HTTP_201_CREATED, 'message':'Customer Created Successfully', 'customer_info':customer_serializer.data})
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'Something is wrong'}, status=status.HTTP_400_BAD_REQUEST)    

## mobile validation number for bangladesh start
import re
def validateMobile(mobile):
    pattern = re.compile('(^([+]{1}[8]{2}|0088)?(01){1}[3-9]{1}\d{8})$') 
    if pattern.match(mobile):
        return True
    else:
        return False
## mobile validation number for bangladesh end    

## for customer registration view end    
    
## plans activation and payment view start      
@api_view(['POST'])
def CustomerSubcriptionPay(request):
    try:
        dial_number = request.data['dial_number'] 
        phone_number = request.data['phone_number'] 
    
        val_mobile = validateMobile(phone_number)
        print('55')
        if not PlansModel.objects.filter(dial_number=dial_number).exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Dial number is not valid!"}, status=status.HTTP_400_BAD_REQUEST)
        if val_mobile==False:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Mobile Number is not valid!"}, status=status.HTTP_400_BAD_REQUEST)
        if not Customer.objects.filter(phone_number=phone_number).exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Not Found mobile number in database!"}, status=status.HTTP_400_BAD_REQUEST)
    
        print('69')
        plan_activate_dial = PlansModel.objects.get(dial_number=dial_number)
        customer_phone_number = Customer.objects.get(phone_number=phone_number)
    
        print('73', plan_activate_dial.per_month_pay_bd_taka)
        print('74', plan_activate_dial.plan_active)
        print('75', customer_phone_number.phone_number)
    
       
    
        if plan_activate_dial.plan_active==True:
            ## ssl commerce 
            sslcz = SSLCOMMERZ({ 'store_id': 'lalco6354730f6ac56', 'store_pass': 'lalco6354730f6ac56@ssl', 'issandbox': True })
            data = {
                    'total_amount': plan_activate_dial.per_month_pay_bd_taka,
                    'currency': "BDT",
                    'tran_id': "tran_12345",
                    'success_url': "http://localhost:8000/api/customer-subscription-pay/", # if transaction is succesful, user will be redirected here
                    'fail_url': "http://localhost:8000/api/customer-subscription-pay/", # if transaction is failed, user will be redirected here
                    'cancel_url': "http://localhost:8000/api/customer-subscription-pay/", # after user cancels the transaction, will be redirected here
                    'emi_option': "0",
                    'cus_name': customer_phone_number.first_name,
                    'cus_email': "test@test.com",
                    'cus_phone': customer_phone_number.phone_number,
                    'cus_add1': "customer address",
                    'cus_city': "Dhaka",
                    'cus_country': "Bangladesh",
                    'shipping_method': "NO",
                    'multi_card_name': "",
                    'num_of_item': 1,
                    'product_name': plan_activate_dial.plan_name,
                    'product_category': "Test Category",
                    'product_profile': "general",
                }
                        
            response = sslcz.createSession(data)
            print('104', response)
            print('105', response['status'])
            
            if response['status'] == 'SUCCESS':
                plan_customer_buy_pay = PlanCustomerBuyPay.objects.create(customer=customer_phone_number, plans_offer=plan_activate_dial, per_month_pay_bd_amount=plan_activate_dial.per_month_pay_bd_taka, plan_active=True, paid=True)
                plan_customer_buy_pay.save()
            
                serializer = PlanCustomerBuyPaySerializer(plan_customer_buy_pay, many=False)
                return Response({'status':status.HTTP_201_CREATED, 'message':'Your Service Activated Successfully', 'service_info':serializer.data})
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'Payment is failed'})
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'Something is wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
## plans activation and payment view end
   
## Service Activation validation check view start    
@api_view(['GET'])   
def Service_Provide_Validate_Check(request, phone_number):
    try:
        service_check = PlanCustomerBuyPay.objects.get(customer__phone_number=phone_number)
        print('124', service_check.plan_active)
        offer_activation_date = service_check.offer_activation_date
        service_provide_day_count = (((datetime.now().date()) - offer_activation_date).days)+1
        print('127', service_provide_day_count)
        if service_provide_day_count <= 30 and service_check.plan_active == True:
            serializer = PlanCustomerBuyPaySerializer(service_check, many=False)
            return Response({'message':'Your Service is activated', 'service_check':serializer.data})
        else:
            service_check.plan_active = False
            service_check.save()
            serializer = PlanCustomerBuyPaySerializer(service_check, many=False)
            return Response({'message':'Your Service is not activated.Please activate your service now!', 'service_check':serializer.data})
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'Something is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            
## Service Activation validation check view end            