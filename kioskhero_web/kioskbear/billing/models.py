from django.db import models


class Price(models.Model):
    currency = models.CharField(max_length=4)
    price = models.PositiveSmallIntegerField()
    billing_cycle = models.CharField(max_length=16)

    def __str__(self):
        return '%s %s %s' % (self.currency, self.price, self.billing_cycle)


class Plan(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name
