from django.urls import path

from practicaltestapp.views import *

urlpatterns = [
    path('customer-register/', CustomerRegistration, name='customer_register'),
    path('customer-subscription-pay/', CustomerSubcriptionPay, name='customer_subscription_pay'),
    path('service-provide-validate-check/<str:phone_number>/', Service_Provide_Validate_Check, name='Service_Provide_Validate_Check'),
]
