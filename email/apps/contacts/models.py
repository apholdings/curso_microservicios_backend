from django.db import models
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    budget = models.CharField(max_length=100,blank=True)
    contact_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.email