from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog

# Create your models here.

class Users(models.Model):
    user = models.ForeignKey(User, blank=False)
    blog_id = models.ForeignKey(Blog)
    token = models.CharField(max_length=50, default="default")

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.username)