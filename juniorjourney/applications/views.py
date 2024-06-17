from django.shortcuts import render, redirect
from .models import Application
from django.contrib.auth.decorators import login_required
from . import forms
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


@login_required(login_url="/users/login/")
def create_job_application(request):
    if request.method == "POST":
        print("post application")
        form = forms.CreateApplication(request.POST, request.FILES)
        if form.is_valid():
            # save new post with user
            new_application = form.save(commit=False)
            new_application.author = request.user
            new_application.save()
            return redirect('applications:list')
        else:
            print('form not valid')
    else:
        form = forms.CreateApplication()
    return render(request, 'applications/new_application.html', {'form': form})


@login_required(login_url="/users/login/")
def applications_list(request):

    try:
        applications = Application.objects.filter(author_id=request.user.id)
    except ObjectDoesNotExist:
        applications = None

    return render(request, "applications/application-list.html", {"applications": applications})


@login_required(login_url="/users/login")
def application_page(request, app_id):
    print(app_id)
    try:
        application = get_object_or_404(Application, id=app_id)
    except ObjectDoesNotExist:
        print("not found")
        application = None
    return render(request, 'applications/application_page.html', {"application": application})

@login_required(login_url="/users/login")
def application_delete(request):
    print("here delete")
    if request.method == "POST":
        try:
            application_id = request.POST.get('application_id', None)

            # application = Application.objects.get(id = application_id)
            Application.objects.filter(id= application_id).delete()
            return JsonResponse({"status":"success", "message": None})
        
        except ObjectDoesNotExist as err:
            return JsonResponse({"status":"error", "message":err.message})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


'''
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

'''