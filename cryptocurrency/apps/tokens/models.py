from django.core.validators import MinValueValidator
from django.db import models

class Token(models.Model):
    ETHEREUM = 'Ethereum'
    POLYGON = 'Polygon'
    NETWORK_CHOICES = (
        (ETHEREUM, 'Ethereum'),
        (POLYGON, 'Polygon'),
    )
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    decimals = models.IntegerField()
    icon_url = models.URLField(blank=True)
    is_custom = models.BooleanField(default=False, blank=True)
    network = models.CharField(max_length=255, choices=NETWORK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class TokenBalance(models.Model):
    wallet = models.CharField(max_length=255,blank=True, null=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='balances')
    balance = models.DecimalField(max_digits=40, decimal_places=18, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('wallet', 'token')


class TokenList(models.Model):
    address = models.CharField(max_length=255,blank=True, null=True)
    tokens = models.ManyToManyField(Token, blank=True)


class NFT(models.Model):
    nft_id = models.IntegerField(unique=True)
    ticket_id = models.CharField(max_length=255,blank=True, null=True)
    ticket_address = models.CharField(max_length=255,blank=True, null=True)
    transaction_hash = models.CharField(max_length=255,blank=True, null=True)


class NFTList(models.Model):
    wallet = models.CharField(max_length=255,blank=True, null=True)
    nfts = models.ManyToManyField(NFT, blank=True)



