from django.contrib import admin
from .models import Author, Post, ViewCount, Rate

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'picture')
    search_fields = ('username', 'email')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at', 'status', 'get_rating', 'get_no_rating', 'get_category_name', 'category', 'sub_category', 'topic')
    list_filter = ('status', 'category', 'sub_category', 'topic', 'author', 'created_at')
    search_fields = ('title', 'author__username', 'keywords')
    autocomplete_fields = ('author', 'category', 'sub_category', 'topic')
    readonly_fields = ('get_rating', 'get_no_rating', 'get_category_name')

class ViewCountAdmin(admin.ModelAdmin):
    list_display = ('post', 'ip_address')
    search_fields = ('post__title', 'ip_address')

class RateAdmin(admin.ModelAdmin):
    list_display = ('rate_number', 'user', 'post')
    search_fields = ('user', 'post__title')
    autocomplete_fields = ('post',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ViewCount, ViewCountAdmin)
admin.site.register(Rate, RateAdmin)