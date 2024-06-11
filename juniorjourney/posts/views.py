from django.shortcuts import render,redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
import json
from juniorjourney.producer import produce_msg

# Create your views here.

@login_required(login_url="/users/login/")
def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html',{ 'posts':posts})

@login_required(login_url="/users/login/")
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html',{ 'post': post})

@login_required(login_url="/users/login/")
def create_post(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST)
        if form.is_valid():
            # save new post with user
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            # new_post_notify(user_id=request.user.id, username=request.user.username,post_title=new_post.title, post_slug=new_post.slug,date=new_post.date)
            return redirect('posts:list')
    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', {'form': form})

# def new_post_notify(user_id, username,post_title,post_slug,date):
#     key = "new_post"
#     value = json.dumps({
#         "pub_id": user_id,
#         "pub_name": username,
#         "post" : {
#             "title": post_title,
#             "slug" : post_slug,
#         },
#         "date": date.isoformat()
#     })
#     produce_msg(topic="notifications_topic",key=key,value=value)
