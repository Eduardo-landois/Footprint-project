from django.urls import path
from . import views

# These live under /runs/ (see config/urls.py)
urlpatterns = [
    path('', views.run_list, name='run_list'),
    path('add_run/', views.add_run, name='add_run'),
    path('<int:run_id>/edit/', views.edit_run, name='edit_run'),
    path('<int:run_id>/delete/', views.delete_run, name='delete_run'),
]
