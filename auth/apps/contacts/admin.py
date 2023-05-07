from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(SellerContact)
admin.site.register(InstructorContact)
admin.site.register(FriendContact)
admin.site.register(SellerContactList)
admin.site.register(InstructorContactList)
admin.site.register(FriendContactList)