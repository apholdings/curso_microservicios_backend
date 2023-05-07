from django.db import models
from django.conf import settings
from djoser.signals import  user_registered



class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_contacts')
    contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_contacted_by')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        unique_together = ('user', 'contact')

class SellerContact(Contact):
    class Meta:
        verbose_name_plural = "Seller Contacts"

class InstructorContact(Contact):
    class Meta:
        verbose_name_plural = "Instructor Contacts"

class FriendContact(Contact):
    class Meta:
        verbose_name_plural = "Friend Contacts"


class SellerContactList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(SellerContact, blank=True)

    def __str__(self):
        return self.user.username + "'s Seller Contacts"

class InstructorContactList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(InstructorContact, blank=True)

    def __str__(self):
        return self.user.username + "'s Instructor Contacts"

class FriendContactList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(FriendContact, blank=True)

    def __str__(self):
        return self.user.username + "'s Friend Contacts"
    

def post_user_registered(request, user ,*args, **kwargs):
    #1. Definir usuario que ser registra
    user = user
    FriendContactList.objects.create(user=user)
    InstructorContactList.objects.create(user=user)
    SellerContactList.objects.create(user=user)

user_registered.connect(post_user_registered)