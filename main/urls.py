from django.urls import path
from main.views import *

urlpatterns = [
    path('add/', newRenter, name='add'),
    path('list/', listRenters, name='list'),
    path('details/<int:id>/', detailRenter, name='details'),
    path('delete/<int:id>/', deleteRenter, name='delete'),
    path('edit/<int:id>/', editRenter, name='edit'),
    path('sendPayment/<int:id>/', sendPayment, name='sendPayment'),
]
