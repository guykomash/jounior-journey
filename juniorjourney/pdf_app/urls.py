from django.urls import path
from . import views


app_name = 'pdf_app'

urlpatterns = [

    path('', views.upload_pdf, name='upload_pdf'),
    path('success/', views.success, name='success'),
]