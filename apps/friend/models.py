from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django_extensions.db.fields import ShortUUIDField


# Create your models here.
class Friend(SoftDeletableModel, TimeStampedModel):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2')
    connection_key = ShortUUIDField(null=True, unique=True)
