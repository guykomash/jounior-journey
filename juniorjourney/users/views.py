from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
import json
import datetime
from django.utils import timezone


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("posts:list")
    else:    
        form = UserCreationForm()
    return render(request, 'users/register.html',{ 'form': form })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            print(form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else: return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html',{ 'form': form })

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")



# def analytics_login(username):
#     key = "subscriptions"
#     value = json.dumps({
#         "user_id": "1",
#         "username": username,
#         "login_time": timezone.now().isoformat(), 

#     })
#     producer.produce("notifications_topic", key=key, value=value)
#     print(f"Produced message to notifications_topic: key = {key:12} value = {value:12}")
#     # send any outstanding or buffered messages to the Kafka broker
#     producer.flush()