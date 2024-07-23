from django.urls import path
from . import views


app_name = 'pdf_app'

urlpatterns = [

    path('', views.pdf_home, name='pdf_home'),
    path('success/', views.success, name='success'),
]