from django.contrib import admin
from .models import Shipping


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', )
    list_display_links = ('title', )
    list_editable = ('price', )
    search_fields = ('title', )
    list_per_page = 25


admin.site.register(Shipping, ShippingAdmin)