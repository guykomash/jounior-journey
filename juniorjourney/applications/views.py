from django.shortcuts import render,redirect
from .models import Application
from django.contrib.auth.decorators import login_required
from . import forms
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

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
            return redirect('/')
        else:
            print('form not valid')
    else:
        form = forms.CreateApplication()
    return render(request, 'applications/new_application.html', {'form': form})

@login_required(login_url="/users/login/")
def applications_list(request):

    try:
        applications = Application.objects.filter(author_id = request.user.id)
    except ObjectDoesNotExist:
        applications = None

    return render(request,"applications/application-list.html",{"applications":applications})
        

