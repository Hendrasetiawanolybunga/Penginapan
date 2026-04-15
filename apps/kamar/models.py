from django.db import models
from core.models import TimeStampedModel
from django.core.validators import MinValueValidator
from decimal import Decimal

class TipeKamar(TimeStampedModel):
    idtipekamar = models.AutoField(primary_key=True)
    namaTipekamar = models.CharField(max_length=50)
    hargaKamar = models.DecimalField(
        max_digits=12, decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))] 
    )
    fasilitas = models.TextField()

    def __str__(self):
        return self.namaTipekamar

class KamarStatus(models.TextChoices):
    TERSEDIA = 'Tersedia', 'Tersedia'
    TERISI = 'Terisi', 'Terisi'
    PERAWATAN = 'Perawatan', 'Perawatan'

class Kamar(TimeStampedModel):
    nomorKamar = models.CharField(primary_key=True, max_length=10)
    posisiLantai = models.IntegerField()
    keteranganKondisi = models.CharField(max_length=255)
    statusKamar = models.CharField(
        max_length=50, 
        choices=KamarStatus.choices, 
        default=KamarStatus.TERSEDIA
    )
    idTipeKamar = models.ForeignKey(TipeKamar, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nomorKamar} - {self.idTipeKamar.namaTipekamar} ({self.statusKamar})'