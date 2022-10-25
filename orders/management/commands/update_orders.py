from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from orders.models import Order


class Command(BaseCommand):
    help ='Updates the orders, puts created as stale after 2 days'

    def handle(self, *args, **kwargs):
        due_date = datetime.now() - timedelta(days=2)
        qs = Order.objects.filter(status='created').filter(created_at__lt=due_date)
        qs.update(status='stale')
        print("Successfully updated")