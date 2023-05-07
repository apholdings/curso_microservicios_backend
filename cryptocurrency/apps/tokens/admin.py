from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.TokenList)
class TokenListAdmin(admin.ModelAdmin):
    list_display = ('address',)
    search_fields = ('address', )
    readonly_fields = ('address','tokens', )

@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name',
'symbol',
'address',
'icon_url',)
    search_fields = ('name',
'symbol',
'address',
'icon_url','decimals', )
    

@admin.register(models.NFTList)
class NFTListAdmin(admin.ModelAdmin):
    list_display = ('wallet',)
    search_fields = ('wallet', )

@admin.register(models.NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ('nft_id','ticket_id','ticket_address',)
    search_fields = ('nft_id','ticket_id','ticket_address', )
