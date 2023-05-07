from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.FriendList)
class FriendsListAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)

@admin.register(models.FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user','timestamp',)
    search_fields = ('from_user','to_user','timestamp',)

    

