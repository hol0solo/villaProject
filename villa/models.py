import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ApartmentCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area = models.PositiveIntegerField()
    floor = models.CharField(max_length=50)
    parking_places = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images')
    when_was_built = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to=ApartmentCategory, on_delete=models.CASCADE)
    stripe_object_price_id = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name

    def create_stripe_object_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_object_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price),
            currency="usd",
        )
        return stripe_object_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_object_price_id:
            stripe_product = self.create_stripe_object_price()
            self.stripe_object_price_id = stripe_product['id']
        super(Apartment, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    class Meta:
        ordering = ['id']


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum_price() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def create_line_items(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.apartment.stripe_object_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    apartment = models.ForeignKey(to=Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return 'В Корзине {} для {}'.format(self.apartment.name, self.user.username)

    def sum_price(self):
        return self.apartment.price * self.quantity

    def de_json(self):
        basket_item = {
            'apartment_name': self.apartment.name,
            'quantity': self.quantity,
            'price': float(self.apartment.price),
            'total_sum': float(self.sum_price()),
        }
        return basket_item
