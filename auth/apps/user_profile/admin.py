from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'url', 'birthday')
    search_fields = ('user__email', 'user__username', 'location')
    list_filter = ('location',)
    readonly_fields = ('picture', 'banner')

    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Images', {'fields': ('picture', 'banner')}),
        ('Personal Information', {'fields': ('location', 'url', 'birthday', 'profile_info')}),
        ('Social Media', {'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'github')}),
    )

admin.site.register(Profile, ProfileAdmin)