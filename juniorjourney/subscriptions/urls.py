from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscriptions, name="subscriptions"),
    path('subscribe/',views.sub_to_user,name="sub")
    # path('/<str:users>/',views.subscriptions_search, name = "subscriptions_search")
]
