from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import generate_id, generate_rid
from .managers import UserManager


class BaseModel(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class User(AbstractUser):

    uid = models.CharField(default=generate_id, max_length=32, unique=True)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class FilePDF(models.Model):
    
    pdf = models.FileField(upload_to="receipts")


class Receipt(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rid = models.CharField(max_length=11, default=generate_rid, unique=True)
    payload = models.JSONField()
    files = models.ManyToManyField(FilePDF)






