from django.contrib import admin
from .models import Rating, ScoredOption, Option

admin.site.register(Rating)
admin.site.register(ScoredOption)
admin.site.register(Option)
