from django.db import models
from core.models import TimeStampedModel
from apps.guest.models import Guest
from apps.kamar.models import Kamar
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

class StatusPembayaran(models.TextChoices):
    DIBAYAR = 'Dibayar', 'Dibayar'
    LUNAS = 'Lunas', 'Lunas'
    BELUM_LUNAS = 'Belum Lunas', 'Belum Lunas'

class MetodeBayar(models.TextChoices):
    TRANSFER = 'Transfer', 'Transfer'
    CASH = 'Cash', 'Cash'

class Pemesanan(TimeStampedModel):
    idPesan = models.AutoField(primary_key=True)
    idGuest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    tanggalPesan = models.DateField(auto_now=True)
    tanggalCheckin = models.DateField()
    tanggalCheckout = models.DateField()
    diskon = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    totalBayar = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    statusPembayaran = models.CharField(
        max_length=50, choices=StatusPembayaran.choices, default=StatusPembayaran.BELUM_LUNAS
    )
    metodeBayar = models.CharField(
        max_length=50, choices=MetodeBayar.choices, default=MetodeBayar.TRANSFER
    )

    @property
    def jumlah_hari(self):
        if self.tanggalCheckin and self.tanggalCheckout:
            return (self.tanggalCheckout - self.tanggalCheckin).days
        return 0

    def perbarui_kalkulasi(self):
        semua_detail = self.detailpemesanan_set.all()
        total_harga_kamar = sum(detail.subTotal for detail in semua_detail if detail.subTotal)
        
        
        persen_diskon = 0
        if self.idGuest.status.lower() == 'member' or self.jumlah_hari >= 14:
            persen_diskon = self.idGuest.idTipeGuest.persenDiskon
            if persen_diskon == 0:
                persen_diskon = 10
                
        
        nilai_diskon = total_harga_kamar * (Decimal(persen_diskon) / Decimal('100'))
        total_akhir = total_harga_kamar - nilai_diskon
        
        
        self.diskon = nilai_diskon
        self.totalBayar = total_akhir
        self.save(update_fields=['diskon', 'totalBayar'])

    def __str__(self):
        return f'{self.idPesan} - {self.idGuest.namaGuest}'
    
class DetailPemesanan(TimeStampedModel):
    idDetail = models.AutoField(primary_key=True)
    idPesan = models.ForeignKey(Pemesanan, verbose_name=_("Pemesanan"), on_delete=models.CASCADE)
    nomorKamar = models.ForeignKey(Kamar, verbose_name=_("Kamar"), on_delete=models.CASCADE)
    subTotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])

    def save(self, *args, **kwargs):
        if self.nomorKamar and self.idPesan:
            harga = self.nomorKamar.idTipeKamar.hargaKamar
            durasi = self.idPesan.jumlah_hari
            self.subTotal = harga * Decimal(durasi)
            
        super().save(*args, **kwargs)
        
        
        self.idPesan.perbarui_kalkulasi()

    def delete(self, *args, **kwargs):
        pesanan_induk = self.idPesan
        super().delete(*args, **kwargs)
        
        
        pesanan_induk.perbarui_kalkulasi()

    def __str__(self):
        return f'{self.idDetail} - {self.nomorKamar.idTipeKamar.namaTipekamar}'