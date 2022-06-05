from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.http import request

# Create your models here.
class Blog_Post(models.Model):
    sl_no = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog/images', blank=True)
    slug = models.SlugField(max_length=420, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['is_approved']

class Blog_Comment(models.Model):
    sl_no = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog_Post, on_delete=models.CASCADE)
    parrent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment + " by "+ self.user.username
    
# Slug Secction
from django.dispatch import receiver
from django.db.models.signals import pre_save
from Blog_App.make_slug import unique_slug_generator
@receiver(pre_save, sender=Blog_Post)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
	    instance.slug = unique_slug_generator(instance)

class Contacts(models.Model):
    sl_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14, default='+880', blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# User profile models on database
class User_Profile(models.Model):
    sn_no = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/avatars', blank=True)
    auth_token = models.CharField(max_length=150)
    # is_verified default true because verify user automatically
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    