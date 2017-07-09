from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from lipame.lipa.utils import do_merchant_payment
from wallet.models import Wallet


@csrf_exempt
def topup(request):
    amount = request.POST.get('topup_amount')
    msisdn = request.user.phone_number.as_e164.replace('+', '')
    response = do_merchant_payment(msisdn, amount).json()
    if response['transactionStatus'] == '200':
        payment_reference = response['transactionReference']
        balance = Wallet.credit_user(request.user, amount, payment_reference)
        status = 'Success'
    else:
        balance = Wallet.user_balance(request.user)
        status ='Failed'

    return JsonResponse({"status": status, "balance": str(balance)+' TZS', "message": response['descriptionText']})
