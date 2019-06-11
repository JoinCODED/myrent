from django.shortcuts import render,redirect,get_object_or_404
from main.models import Renter
from django.urls import reverse
from transactions.models import Transaction
import json
import requests
from django.utils import timezone
from django.db.models import Q
from datetime import datetime

def transactionList(request,id):
    renter = get_object_or_404(Renter, id=id)
    if request.user != renter.landlord:
        return redirect('list')
    transactions = Transaction.objects.filter(renter=renter)
    context = {
        'transactions': transactions
    }
    return render(request,'transactions/list.html', context)

def newTransactions(request):
    user = request.user
    transactions = Transaction.objects.filter(renter__landlord=user,date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0))
    context = {
        'transactions': transactions
    }
    return render(request,'transactions/list.html', context)

def failToPay(request):
    user = request.user
    now = datetime.now()
    year, month, *args = now.timetuple()
    last_paid = "{0}-{1}".format(year,month)
    renters = Renter.objects.filter(landlord=user).exclude(last_paid=last_paid)
    context = {
        'renters': renters
    }
    return render(request, 'transactions/failToPay.html', context)

def collected(request):
    user = request.user
    transactions = Transaction.objects.filter(renter__landlord=user,date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).filter(status="CAPTURED")
    total = 0
    for transaction in transactions:
        total = total + float(transaction.amount)
    context = {
        'total': total,
        'transactions': transactions
    }
    return render(request, 'transactions/collected.html', context)

def pay(request,token):
    renter = get_object_or_404(Renter, token=token)
    url = request.build_absolute_uri('/')[:-1].strip("/") + reverse('response')
    response = tap(renter,url)
    paymentUrl = response['transaction']['url']
    return redirect(paymentUrl)

def responsePage(request):
    tapId = request.GET.get('tap_id')
    context = {}
    transaction = Transaction.objects.filter(tapId=tapId).first()
    if transaction is not None:
        context['transaction'] = transaction
    if tapId and transaction is None:
        jsonResponse = checkpayment(tapId)
        renter = Renter.objects.get(token=jsonResponse.get('metadata').get('udf2'))
        transaction = Transaction(
                        tapId=jsonResponse.get('id'),
                        status=jsonResponse.get('status'),
                        amount=jsonResponse.get('amount'),
                        currency=jsonResponse.get('currency'),
                        transactionId=jsonResponse.get('transaction').get('authorization_id'),
                        trackId=jsonResponse.get('reference').get('track'),
                        paymentId=jsonResponse.get('reference').get('payment'),
                        renter=renter
                        )
        transaction.save()
        renter.paid()
        renter.generate_url()
        context['transaction'] = transaction
    return render(request, 'transactions/result.html', context)

def checkpayment(tapId):
    url = "https://api.tap.company/v2/charges/{0}".format(tapId)
    headers = {'authorization': 'Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ'}
    response = requests.request("GET", url, headers=headers)
    jsonResponse = json.loads(response.text)
    return jsonResponse

def tap(renter,url):
    payload =  {
            "amount": str(renter.amount),
            "currency":"KWD",
            "threeDSecure":"true",
            "save_card":"false",
            "description":
            "Rental Payment",
            "statement_descriptor":"Rent",
            "metadata":{
                "udf1":
                str(renter.phone),
                "udf2":
                str(renter.token)
                },
            "customer": {
                "first_name": str(renter.name),
                "phone": {
                    "country_code": "965",
                    "number": str(renter.phone)
                }
            },
            "source": {
                "id": "src_all"
            },
            "redirect": {
                "url": url
            }
        }
    payload = json.dumps(payload)
    headers = {
    'authorization': "Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ",
    'content-type': "application/json"
    }
    response = requests.request("POST", "https://api.tap.company/v2/charges", data=payload, headers=headers)
    jsonResponse = json.loads(response.text)
    return jsonResponse
