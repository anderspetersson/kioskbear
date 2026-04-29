from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from ..kiosk.views import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("kioskbear.landingpages.urls", namespace="landingpages")),
    path("accounts/", include("kioskbear.accounts.urls", namespace="accounts")),
    path("app/", include("kioskbear.app.urls", namespace="app")),
    path("api/v1/", api.urls),
]

urlpatterns += staticfiles_urlpatterns()
