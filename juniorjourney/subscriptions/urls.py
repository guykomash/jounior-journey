from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscriptions, name="subscriptions"),
    # path('/<str:users>/',views.subscriptions_search, name = "subscriptions_search")
]
