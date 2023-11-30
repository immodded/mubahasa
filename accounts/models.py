from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    about = models.CharField(max_length=50, default='None')
    TYPE_OPTIONS = (
        ('Free','Free'),
        ('Premium','Premium'),
    )
    type = models.CharField(max_length=8,choices=TYPE_OPTIONS,default='Free')
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)

    def __str__(self):
        if self.user:
            return str(self.user.username)
        return str(self.name)
    def get_absolute_url(self):
        """
        Get the absolute URL for the patient's detail view.
        """
        return reverse("user_profile_detail", kwargs={"pk": self.id})

