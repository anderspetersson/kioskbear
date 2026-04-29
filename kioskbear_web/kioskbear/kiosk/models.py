from django.db import models


class Survey(models.Model):
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default='My store')
    type = models.CharField(max_length=64, default='feedback')
    start_block = models.ForeignKey('Block', on_delete=models.SET_NULL, null=True, blank=True, related_name='surveys')
    end_block = models.ForeignKey('Block', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return self.name


class Block(models.Model):
    survey = models.ForeignKey('kiosk.Survey', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title