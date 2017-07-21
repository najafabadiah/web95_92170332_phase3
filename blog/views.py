from django.shortcuts import render
from .models import *
from auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Create your views here.

@csrf_exempt
def posts(request, blog_id):
    try:
        token = request.META['HTTP_MYTOKEN']
        if token is None:
            return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)
        author = Users.objects.get(user=request.user)
        if token != author.token:
            return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)

        blog = Blog.objects.filter(id=blog_id)

        if request.method == 'GET':
            post_list = []

            for post in Post.objects.filter(blog=blog):
                post_list.append(model_to_dict(post))

            return JsonResponse(data={'status': 0, 'posts': post_list}, safe=False)
        else:
            return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)

    except:
        return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)

@csrf_exempt
def post(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    token = request.META['HTTP_MYTOKEN']
    if token is None:
        return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)

    author = Users.objects.get(user=request.user)
    if token != author.token:
        return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)

    if request.method == 'GET':
        id = request.GET['id']
        post = Post.objects.get(post_id=id)
        response = {
            'id': post.post_id,
            'title': post.title,
            'summery': post.summary,
            'datetime': post.datetime,
            'text': post.text
        }
        return JsonResponse(data={'status': 0, 'post': response}, safe=False)

    if request.method == 'POST':
        post = Post()
        post.blog_id = blog.blog_id
        post.title = request.POST['title']
        post.summary = request.POST['summary']
        post.text = request.POST['text']
        post.save()
        return JsonResponse(data={'status': 0}, safe=False)
    else:
        return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)


@csrf_exempt
def comments(request, post_id):
    try:
        token = request.META['HTTP_MYTOKEN']
        if token is None:
            return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)
        author = Users.objects.get(user=request.user)
        if token != author.token:
            return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)

        if request.method == 'GET':
            comment_list = []

            for comment in Comment.objects.filter(post_id=post_id):
                comment_list.append(model_to_dict(comment))
            return JsonResponse(data={'status': 0, 'comments': comment_list}, safe=False)
        else:
            return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)

    except:
        return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)


@csrf_exempt
def comment(request, post_id):
    try:
        token = request.META['HTTP_MYTOKEN']
        if token is None:
            return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)

        author = Users.objects.get(user=request.user)
        if token != author.token:
            return JsonResponse(data={'status': -1, 'message': 'no/wrong token'}, safe=False)

        if request.method == 'POST':
            comment = Comment()
            comment.post_id = post_id
            comment.text = request.POST['text']
            comment.save()

            return JsonResponse(data={'status': 0}, safe=False)
        else:
            return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)

    except:
        return JsonResponse(data={'status': -1, 'message': "Something wrong!"}, safe=False)