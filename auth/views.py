from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .forms import *
import random, string

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import *
from blog.models import Blog

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            author = Users()
            author.user = user

            newBlog = Blog()
            newBlog.save()

            author.blog_id = newBlog.id
            author.save()

            newBlog.owner = author
            newBlog.save()

            return JsonResponse(data={'status': 0}, safe=False )
        else:
            return JsonResponse(data={'status': -1}, safe=False)

    else:
        return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            token = ''.join([random.choice(string.ascii_lowercase) for i in range(20)])
            author = Users.objects.get(user=user)
            author.token = token
            author.save()
            return JsonResponse(data={'status': 0, 'token': token}, safe=False)
        else:
            return JsonResponse(data={'status': -1}, safe=False)
    else:
        return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)


def default_blog(request):
    token=request.META.__getitem__('HTTP_MYTOKEN')
    if request.method == 'GET':
        author = Users.objects.get(token=token)
        blog_id = author.blog_id
        return JsonResponse(data={'status': 0, 'id': blog_id}, safe=False)
    else:
        return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)