from django.db import models

from users.models import User
from villa.models import Basket


class PreOrder(models.Model):
    CREATED = 0
    RESERVED = 1
    PAID = 2
    OBSERVED = 3
    PREPARED = 4
    READY = 5
    STATUSES = (
        (CREATED, 'Created'),
        (RESERVED, 'Reserved'),
        (PAID, 'Paid'),
        (OBSERVED, 'Observed'),
        (PREPARED, 'Prepared'),
        (READY, 'Ready'),
    )

    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20)
    agent = models.CharField(max_length=100)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    basket_history = models.JSONField(default=dict)

    def __str__(self):
        return f'PreOrder for {self.name} {self.surname} from {self.initiator.username}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
