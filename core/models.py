import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} | {self.creator.username}"

    def get_absolute_url(self):
        return reverse("Discussion_detail", kwargs={"pk": str(self.id)})

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.creator.username} | {self.created_at}"
 

    def get_absolute_url(self):
        return reverse("Message_detail", kwargs={"pk": str(self.id)})


class Like(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)        
