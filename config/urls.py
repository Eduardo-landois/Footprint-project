from django.contrib import admin
from django.urls import include, path

from accounts import views as account_views

urlpatterns = [
    path("", account_views.home, name="home"),
    path("admin/", admin.site.urls),
    # Our account pages (signup, profile, manage users)
    path("accounts/", include("accounts.urls")),
    # Django's built-in login/logout pages
    path("accounts/", include("django.contrib.auth.urls")),
]
