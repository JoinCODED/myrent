from django.db import models
from main.models import Renter

class Transaction(models.Model):
    tapId = models.CharField(max_length=250,null=True,blank=True)
    status = models.CharField(max_length=250,null=True,blank=True)
    amount = models.CharField(max_length=250,null=True,blank=True)
    currency = models.CharField(max_length=250,null=True,blank=True)
    transactionId = models.CharField(max_length=250,null=True,blank=True)
    trackId = models.CharField(max_length=250,null=True,blank=True)
    paymentId = models.CharField(max_length=250,null=True,blank=True)
    renter = models.ForeignKey(Renter,on_delete=models.CASCADE,related_name="transaction")
    date = models.DateTimeField(auto_now=False,auto_now_add=True)
    
    def __str__(self):
        return str(self.renter.amount)
