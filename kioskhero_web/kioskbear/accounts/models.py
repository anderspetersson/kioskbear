from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import AccountManager


class Customer(models.Model):
    organisation_name = models.CharField(max_length=256)
    head_account = models.OneToOneField('Account', related_name='+', null=True, on_delete=models.CASCADE)
    billing_account = models.OneToOneField('Account', related_name='+', null=True, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=256, null=True, blank=True)
    price = models.ForeignKey('billing.Price', on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.ForeignKey('billing.Plan', on_delete=models.SET_NULL, null=True, blank=True)
    trial_expire_date = models.DateField(null=True)
    trial_is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.organisation_name


class Account(AbstractUser):
    username = None
    customer = models.ForeignKey('Customer', null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=256, unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email





