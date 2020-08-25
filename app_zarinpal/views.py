from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from django.http import HttpResponseRedirect
from app_accounts.models import Basket
import datetime
import requests
import urllib.parse

# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 100  # Toman / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'example.com'  # Optional
# mobile = '09123456789'  # Optional
# CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.

@api_view(['GET'])
def send_request(request):
    basket = Basket.objects.get(user=request.user,status='active')
    # مربوط به درگاه پرداخت ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
    email=request.GET.get('email','example.com')
    description=request.GET.get('description','توضیحات مربوط به تراکنش را در این قسمت وارد کنید')
    mobile=int(request.GET.get('mobile',basket.user.username))
    # CallbackURL ='http://localhost:8000/zarinpal/verify/'
    CallbackURL = 'http://127.0.0.1:8000/zarinpal/verify/'
    amount=int(basket.payable_amount)
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if result.Status == 100:
        # تغیرات بسکت ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        basket.status='pardakht'
        basket.order_registration_date=datetime.date.today()
        basket.save()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # return HttpResponseRedirect(redirect_to='https://sandbox.zarinpal.com/pg/StartPay/'+ str(result.Authority))
        return HttpResponse(redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority)).url)
    else:
        return HttpResponse('Error code: ' + str(result.Status))



@api_view(['GET'])
def verify(request):
    basket=Basket.objects.get(user=request.user,status='pardakht')
    mobile = basket.user.username
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
    MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    amount=basket.payable_amount
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms
    main_api = 'https://raygansms.com/SendMessageWithUrl.ashx?'
    mobile = basket.user.username
    mobile = '09123669277'  # چون پوزرنیم من موبایل نیست بعدا درستش کن و اینو حذف کن #################################
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if request.GET.get('Status') == 'OK':
        result =  client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            # import ipdb; ipdb.set_trace()
            basket.status='pardakht-shod'
            basket.position='1'
            basket.save()
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms

            url = main_api + urllib.parse.urlencode(
                {'Username': '09123669277', 'Password': '5989231', 'PhoneNumber': '50002910001080',
                 'MessageBody': f'پرداخت شما موفقیت امیز بود کد بسکت شم{basket.id}', 'RecNumber': mobile, 'Smsclass': '1'})
            requests.get(url).json()
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:

            return HttpResponse('Transaction submitted : ' + str(result.Status))


        else:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms
            url = main_api + urllib.parse.urlencode(
                {'Username': '09123669277', 'Password': '5989231', 'PhoneNumber': '50002910001080',
                 'MessageBody': f' پرداخت شما موفقیت امیز نبود{result.Status}', 'RecNumber': mobile,
                 'Smsclass': '1'})
            requests.get(url).json()
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))

    else:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sms
        url = main_api + urllib.parse.urlencode(
            {'Username': '09123669277', 'Password': '5989231', 'PhoneNumber': '50002910001080',
             'MessageBody': ' پرداخت شما موفقیت امیز نبود', 'RecNumber': mobile,
             'Smsclass': '1'})
        requests.get(url).json()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        return HttpResponse('Transaction failed or canceled by user')