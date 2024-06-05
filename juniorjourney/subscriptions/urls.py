from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subs_dashboard, name="dashboard"),
]
