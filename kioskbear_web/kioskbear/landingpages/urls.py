from django.urls import path
from .views import StartPageView
from django.contrib.auth import views as auth_views
app_name = 'landingpages'

urlpatterns = [
    path('', StartPageView.as_view(), name='index'),
]