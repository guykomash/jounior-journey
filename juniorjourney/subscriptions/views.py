from django.shortcuts import render,redirect
from .models import Subscription
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

@login_required(login_url="/users/login/")
def subs_dashboard(request):
    print("Here")
    my_subs = Subscription.objects.filter(pub_id = request.user.id)
    my_pubs = Subscription.objects.filter(sub_id = request.user.id)
    # return render(request, 'subscriptions/subs_dashboard.html')
    return render(request, 'subs_dashboard.html', {'subs':my_subs, 'pubs':my_pubs})