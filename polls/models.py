from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# # Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True,)
    avatar = models.ImageField(null=True,default="avatar.svg")
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]










class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    update = models.DateTimeField(auto_now=True)
    #auto_now represent the snapshots of every time updated
    #auto_now_add represent the snapshots of once when it created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
    #order by first updated value and then created value
        #'-' prefix update the value in reverse order
         ordering =["-update","-created"]

    
    def __str__(self):
        return self.name

    


class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #on_delete=models.CASCADE attribute will delete all the message related to it when parent deletes
    #on_delete=models.SET_NULL menas message will save database although parent deleted
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
         ordering =["-update","-created"]

    def __str__(self):
        return self.body[0:50]
