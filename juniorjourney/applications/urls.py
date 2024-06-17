from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.applications_list, name="list"),
    path('new-application/', views.create_job_application, name="new-application"),
    path('<int:app_id>', views.application_page, name="page"),
    path('delete/', views.application_delete, name="delete"),

]
