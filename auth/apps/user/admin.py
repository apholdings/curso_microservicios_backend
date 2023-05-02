from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class UserAccountAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'slug', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_online', 'is_staff', 'role', 'verified', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'role', 'verified')
        }),
    )

    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'verified')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('role', 'is_staff', 'is_active', 'verified')
    ordering = ('email',)
    readonly_fields = ('slug',)

admin.site.register(UserAccount, UserAccountAdmin)