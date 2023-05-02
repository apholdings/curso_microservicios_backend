from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'phone', 'contact_date')
    search_fields = ('name', 'email', 'subject', 'phone')
    list_filter = ('contact_date',)
    readonly_fields = ('contact_date',)

    fieldsets = (
        (None, {'fields': ('name', 'email', 'subject', 'phone')}),
        ('Message and Budget', {'fields': ('message', 'budget')}),
        ('Contact Date', {'fields': ('contact_date',)}),
    )

admin.site.register(Contact, ContactAdmin)