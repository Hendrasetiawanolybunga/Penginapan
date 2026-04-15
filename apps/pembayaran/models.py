from django.db import models
from core.models import TimeStampedModel
from apps.pemesanan.models import Pemesanan
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

class DetailPembayaran(TimeStampedModel):
    idDetailBayar = models.AutoField(primary_key=True)
    idPesan = models.ForeignKey(Pemesanan, verbose_name=_("Pemesanan"), on_delete=models.CASCADE)
    jumlahPembayaran = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    buktiBayar = models.ImageField(upload_to='bukti_bayar/')

    def __str__(self):
        return f'Pembayaran {self.idDetailBayar} - Pesanan {self.idPesan.idPesan}'