from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'compare_price',
                    'price', 'stock', 'sold','status' )
    list_display_links = ( 'title', )
    list_filter = ('category', )
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ('compare_price', 'price', 'stock','status' )
    search_fields = ('title', 'description', )
    list_per_page = 25
admin.site.register(Product, ProductAdmin)

class SellersAdmin(admin.ModelAdmin):
    exclude = ('id',)
    readonly_fields = ('author','address',)
admin.site.register(Sellers,SellersAdmin)

admin.site.register(Color)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Rate)
admin.site.register(Details)
admin.site.register(Size)
admin.site.register(Benefits)
admin.site.register(Requisite)
admin.site.register(WhoIsFor)
admin.site.register(Weight)
admin.site.register(Material)