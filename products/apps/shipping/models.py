from django.db import models
import uuid

# Create your models here.
class Shipping(models.Model):
    class Meta:
        verbose_name = 'Shipping'
        verbose_name_plural = 'Shipping List'

    id =                        models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_id =               models.IntegerField(null=True, blank=True)
    title =                     models.CharField(max_length=255)
    author =                    models.UUIDField(blank=True, null=True)
    price =                     models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    time =                      models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title