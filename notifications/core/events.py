from django.utils.dateparse import parse_datetime

def subscription(data):
    print(f"subscription consumed: value = {data}")


def new_post(data):
    print(f"post_publish consumed: value = {data}")

def job_application(data):
    print(f"job_application consumed: value = {data}")
