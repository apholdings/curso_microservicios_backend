from django.contrib import admin
from .models import Wallet

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__username', 'address')
    readonly_fields = ('address','user',)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        fields.remove('private_key')
        return fields

admin.site.register(Wallet, WalletAdmin)