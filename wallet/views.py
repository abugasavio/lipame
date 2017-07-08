from django.http import JsonResponse
from django.shortcuts import render
from wallet.models import Wallet


def topup(request):
    amount = request.POST.get('amount')
    response = do_merchant_payment(msisdn, amount).json()
    if response['status'] == '200':
        balance = Wallet.credit_user(request.user, amount)
        status = 'Success'
    else:
        balance = Wallet.user_balance(request.user)
        status ='Failed'

    return JsonResponse({"status": status, "balance": balance, "message": response['message']})
