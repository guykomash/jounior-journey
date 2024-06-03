from core.models import UserLogin,JobApplication
from django.utils.dateparse import parse_datetime

def user_login(data):
    # UserLogin.objects.create(
    #         user_id = data['user_id'],
    #         username= data['username'],
    #         login_time= parse_datetime(data['login_time']),
    #     )
    print(f"Consumed message: value = {data}")
    
def job_application(data):
    JobApplication.objects.create(
    user_id = data['user_id'],
    username= data['username'],
    comapny_name = data['company_name'],
    job_title = data['job_title'],
    application_date = data['application_date']
)