from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from uuid import uuid4
import plivo
from datetime import datetime

plivo_id = "YOUR_ID"
plivo_token = "YOUR_TOKEN"
client = plivo.RestClient(plivo_id,plivo_token)

class Renter(models.Model):
    phone = models.IntegerField(unique=True)
    amount = models.FloatField()
    landlord = models.ForeignKey(User,on_delete=models.CASCADE,related_name="landlord")
    adressName = models.CharField("Address name",max_length=1024)
    name = models.CharField("Full name",max_length=1024)
    address1 = models.CharField("Address line 1",max_length=1024)
    address2 = models.CharField("Address line 2",max_length=1024,null=True,blank=True)
    zip_code = models.CharField("ZIP / Postal code",max_length=12,null=True,blank=True)
    city = models.CharField("City",max_length=1024)
    country = CountryField("Country")
    token = models.CharField(max_length=250,default=uuid4())
    last_paid = models.CharField(max_length=250,null=True,blank=True)
    def __str__(self):
        return str(self.phone)
    def generate_url(self):
        self.token = uuid4()
        self.save()
        return "https://myrent.codeunicorn.io/pay/{0}".format(self.token)
    def sms(self):
        body = """Your paymet of {1} K.D is due, Pay using the following link {2}""".format(self.name, self.amount,self.generate_url())
        msg = client.messages.create(
            src='+32466900585',
            dst='+965'+str(self.phone),
            text=body,
        )
        return msg
    def paid(self):
        now = datetime.now()
        year, month, *args = now.timetuple()
        self.last_paid = "{0}-{1}".format(year,month)
        self.save()
