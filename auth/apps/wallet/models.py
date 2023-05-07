import secrets, base64, json, rsa, os
from djoser.signals import  user_registered
from core.producer import producer
from django.db import models

from django.conf import settings
import LWE4 as lwe

from eth_account import Account
from web3 import Web3
polygon_rpc = settings.POLYGON_RPC
ethereum_rpc = settings.ETHEREUM_RPC

User = settings.AUTH_USER_MODEL
# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    # Ethereum Wallet
    address = models.CharField(max_length=255)
    private_key = models.JSONField() 


# def test_decryption(user):
#     private_key_path = os.path.join(settings.BASE_DIR, 'private_key.json')
#     with open(private_key_path, "r") as f:
#         private_key = json.load(f)
#     wallet = Wallet.objects.get(user=user)
#     encrypted_private_key = wallet.private_key
#     decrypted_string = json.loads(lwe.decrypt.decrypt(json.loads(encrypted_private_key), private_key))
#     print("Decrypted private key:", decrypted_string)


def create_user_wallet(request, user, *args, **kwargs):
    public_key_path = os.path.join(settings.BASE_DIR, 'public_key.json')
    with open(public_key_path, "r") as f:
        public_key = json.load(f)
    # 1. Crear llaves Publica y Privada de Ethereum
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    # 2. Encriptar llave privada con algoritmo de latices
    encrypted_private_key = lwe.encrypt.encrypt(private_key, public_key)
    Wallet.objects.create(user=user, private_key=encrypted_private_key, address=acct.address)
    # test_decryption(user)

    item = {}
    item['address'] = acct.address
    producer.produce(
        os.environ.get('KAFKA_TOPIC'),
        key='wallet_created',
        value=json.dumps(item).encode('utf-8')
    )
    producer.flush()

user_registered.connect(create_user_wallet)
