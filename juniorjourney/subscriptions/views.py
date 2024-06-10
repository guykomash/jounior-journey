from django.shortcuts import render,redirect
from .models import Subscription
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

@login_required(login_url="/users/login/")
def subscriptions(request):
    search_query = request.GET.get('users')
    if search_query is not None:
        users = User.objects.filter(username__icontains = search_query)
    else: users = []
    my_subs = Subscription.objects.filter(pub_id = request.user.id)
    my_pubs = Subscription.objects.filter(sub_id = request.user.id)
    # return render(request, 'subscriptions/subs_dashboard.html')
    return render(request, 'subs_dashboard.html', {'users': users,'subs':my_subs, 'pubs':my_pubs})

@login_required(login_url="/users/login/")
def sub_to_user(request):
    print("heren")
    if request.method == "POST":
        pub_id = request.POST.get('pub_id', None)
        sub_id = request.POST.get('sub_id', None)

        if pub_id and sub_id:    
            print(f"pub_id = {pub_id}")
            print(f"sub_id = {sub_id}")
            res = {'status': 'success', 'message':'Subscribed successful'}
        else:
            res = {'status':'error', 'message':'No data recieved or partial'}
        return JsonResponse(res)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    

# @login_required(login_url="/users/login/")
# def subscriptions_search(request,users):
#     print("Heren")
#     print(f"users: {users}")
#     return render(request, 'subs_dashboard.html')