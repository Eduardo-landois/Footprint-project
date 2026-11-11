from django.urls import path
from . import views

# These live under /accounts/ (see config/urls.py),
# next to Django's built-in login/ and logout/ URLs.
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/role/', views.change_role, name='change_role'),
]
