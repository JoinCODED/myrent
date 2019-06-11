from django.urls import path
from transactions.views import *

urlpatterns = [
    path('pay/<str:token>/', pay, name='pay'),
    path('response/', responsePage, name='response'),
    path('transactions/<int:id>/', transactionList, name='transactions'),
    path('newTransactions/', newTransactions, name='newTransactions'),
    path('failToPay/', failToPay, name="failToPay"),
    path('collected/', collected, name="collected")

]
