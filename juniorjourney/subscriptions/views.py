from django.shortcuts import render,redirect
from .models import Subscription
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.db.utils import IntegrityError 
# Create your views here.

@login_required(login_url="/users/login/")
def subscriptions(request):
    search_query = request.GET.get('users')
    if search_query is not None:
        users = User.objects.filter(username__icontains = search_query).exclude(id=request.user.id)
    else: users = []
    my_subs = Subscription.objects.filter(pub_id = request.user.id)
    my_pubs = Subscription.objects.filter(sub_id = request.user.id)
    # return render(request, 'subscriptions/subs_dashboard.html')
    return render(request, 'subs_dashboard.html', {'users': users,'subs':my_subs, 'pubs':my_pubs})

@login_required(login_url="/users/login/")
def sub_to_user(request):
    if request.method == "POST":
        try:
            pub_id = request.POST.get('pub_id', None)
            sub_id = request.POST.get('sub_id', None)

            if pub_id == sub_id:
                raise ValidationError("User cannot subscribe to itself")
     
            pub_user = User.objects.get(id = pub_id)
            sub_user = User.objects.get(id = sub_id)

            subscription = Subscription.objects.create(pub=pub_user, sub=sub_user)
            subscription.save()

            print(f"{sub_user.username} subscribing to {pub_user.username}")
            return JsonResponse({"status":"success", "message": f"Subscribed to {pub_user.username} successfuly!"})
        except (ObjectDoesNotExist,ValidationError) as err:
            return JsonResponse({"status":"error", "message":err.message})
        except IntegrityError as err:
            return JsonResponse({"status":"success", "message":"already subscribed"})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
@login_required(login_url="/users/login/")
def unsubscribe_from_user(request):
    if request.method == "POST":
        try:
            pub_id = request.POST.get('pub_id', None)
            sub_id = request.POST.get('sub_id', None)

            if pub_id == sub_id:
                raise ValidationError("User cannot unsubscribe from itself")
     
            pub_user = User.objects.get(id = pub_id)
            sub_user = User.objects.get(id = sub_id)

            subscription = Subscription.objects.get(pub=pub_user, sub=sub_user)
            subscription.save()

            print(f"{sub_user.username} subscribing to {pub_user.username}")
            return JsonResponse({"status":"success", "message": f"Subscribed to {pub_user.username} successfuly!"})


        except (ObjectDoesNotExist,ValidationError) as err:
            return JsonResponse({"status":"error", "message":err.message})
        except IntegrityError as err:
            return JsonResponse({"status":"success", "message":"already subscribed"})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)