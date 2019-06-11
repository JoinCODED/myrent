from django.core.management.base import BaseCommand, CommandError
from main.models import Renter

class Command(BaseCommand):
    help = 'Sends SMS messages to all Renters'

    def handle(self, *args, **kwargs):
        renters = Renter.objects.all()
        for renter in renters:
            renter.sms()
        self.stdout.write(self.style.SUCCESS('Successfully sent SMS to : %s renters') % len(renters))
