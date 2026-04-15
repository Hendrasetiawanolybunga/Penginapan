from django.db import models
from core.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class TipeGuest(TimeStampedModel):
    idTipeGuest = models.AutoField(primary_key=True)
    namaTipeGuest = models.CharField(max_length=50)
    persenDiskon = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)] 
    )

    def __str__(self):
        return self.namaTipeGuest

class GuestStatus(models.TextChoices):
    REGULER = 'Reguler', 'Reguler'
    MEMBER = 'Member', 'Member'

class Guest(TimeStampedModel):
    idGuest = models.AutoField(primary_key=True)
    namaGuest = models.CharField(max_length=50)
    ktp = models.ImageField(upload_to='ktp/', max_length=255)
    status = models.CharField(
        max_length=50, 
        choices=GuestStatus.choices, 
        default=GuestStatus.REGULER
    )
    nomorTelepon = models.CharField(max_length=20)
    idTipeGuest = models.ForeignKey(TipeGuest, verbose_name=_("Tipe Guest"), on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.namaGuest} - ({self.status})'