from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
      return self.name 


class Room(models.Model):
    topic = models.ForeignKey(
        Topic, 
        on_delete=models.SET_NULL,null=True  # Delete all messages when a room is deleted
          
    )
    host = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,null=True  # Delete all messages when a room is deleted
    )
    updated = models.DateTimeField(auto_now=True)  # Auto-updates on every save
    created = models.DateTimeField(auto_now_add=True)  # Sets on creation
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)

    class Meta:
       ordering=['-updated','-created']

    def __str__(self):
      return self.name

  


class Message(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Deletes the message if the related user is deleted
    )
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, null=True # Deletes all messages when the related room is deleted
    )
    body = models.TextField()  # Message content
    updated = models.DateTimeField(auto_now=True)  # Auto-updates on every save
    created = models.DateTimeField(auto_now_add=True)  # Sets on creation

    class Meta:
       ordering=['-updated','-created']


    def __str__(self):
        return self.body[0:50]  # Return the first 50 characters of the message body
