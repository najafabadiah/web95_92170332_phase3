from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    blog_id = models.AutoField(primary_key='true')
    owner = models.ForeignKey(User, default=0)

    def __str__(self):
        return "{0} - {1}".format(self.blog_id, self.owner.username)

class Post(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key='true')
    title = models.CharField(max_length=60)
    summary = models.CharField(max_length=150)
    text = models.CharField(max_length=600)
    datetime = models.DateField(auto_now_add='true')

    def __str__(self):
        return "{0} - {1}".format(self.post_id, self.title)

    @staticmethod
    def create(blog_id, title, summary, text):
        return Post.objects.create(blog_id=blog_id, title=title, summary=summary, text=text)


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    datetime = models.DateField(auto_now_add='true')

    def __str__(self):
        return "{0} - {1}".format(self.post_id, self.text)

    @staticmethod
    def create(post_id, text):
        return Comment.objects.create(post_id=post_id, text=text)