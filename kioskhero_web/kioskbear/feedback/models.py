from django.db import models


class ScoredOption(models.Model):
    block = models.ForeignKey('kiosk.Block', on_delete=models.CASCADE, related_name='scored_options')
    score = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=256)
    follow_up_block = models.ForeignKey('kiosk.Block', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        ordering = ('score',)

    def __str__(self):
        return self.text


class Option(models.Model):
    block = models.ForeignKey('kiosk.Block', on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=256)
    follow_up_block = models.ForeignKey('kiosk.Block', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    def __str__(self):
        return self.text


class FormField(models.Model):
    block = models.ForeignKey('kiosk.Block', on_delete=models.CASCADE)
    field_type = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    label = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Rating(models.Model):
    score = models.PositiveSmallIntegerField()
    survey = models.ForeignKey('kiosk.Survey', on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.score)
