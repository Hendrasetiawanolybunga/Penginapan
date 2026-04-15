from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class TipeKamar(models.Model):
    idtipekamar = models.AutoField(primary_key=True)
    namaTipekamar = models.CharField(max_length=50)
    hargaKamar = models.DecimalField(max_digits=12, decimal_places=2)
    fasilitas = models.TextField()

    def __str__(self):
        return self.namaTipekamar

class Kamar(models.Model):
    nomorKamar = models.CharField(primary_key=True, max_length=10)
    posisiLantai = models.IntegerField()
    keteranganKondisi = models.CharField(max_length=255)
    statusKamar = models.CharField(max_length=50, choices=[
        ('Tersedia', 'Tersedia'),
        ('Terisi', 'Terisi'),
        ('Perawatan', 'Perawatan'),
    ], default='Tersedia')
    idTipeKamar = models.ForeignKey(TipeKamar, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nomorKamar} - {self.idTipeKamar.namaTipekamar} ({self.statusKamar})'

class TipeGuest(models.Model):
    idTipeGuest = models.AutoField(primary_key=True)
    namaTipeGuest = models.CharField(max_length=50)
    persenDiskon = models.IntegerField()

    def __str__(self):
        return self.namaTipeGuest

class Guest(models.Model):
    idGuest = models.AutoField(primary_key=True)
    namaGuest = models.CharField(max_length=50)
    ktp = models.ImageField(upload_to='ktp/', max_length=255)
    status = models.CharField(max_length=50, choices=[
        ('Reguler', 'Reguler'),
        ('Member', 'Member'),
    ], default='Reguler')
    nomorTelepon = models.CharField(max_length=20)
    idTipeGuest = models.ForeignKey(TipeGuest, verbose_name=_("Tipe Guest"), on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.namaGuest} - ({self.status})'

class Pemesanan(models.Model):
    idPesan = models.AutoField(primary_key=True)
    idGuest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    tanggalPesan = models.DateField(auto_now=True)
    tanggalCheckin = models.DateField()
    tanggalCheckout = models.DateField()
    diskon = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    totalBayar = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    statusPembayaran = models.CharField(max_length=50, choices=[
        ('Dibayar', 'Dibayar'),
        ('Lunas', 'Lunas'),
        ('Belum Lunas', 'Belum Lunas'),
    ], default='Dibayar')
    metodeBayar = models.CharField(max_length=50, choices=[
        ('Transfer', 'Transfer'),
        ('Cash', 'Cash'),
    ], default='Transfer')

    @property
    def jumlah_hari(self):
        if self.tanggalCheckin and self.tanggalCheckout:
            return (self.tanggalCheckout - self.tanggalCheckin).days
        return 0

    def __str__(self):
        return f'{self.idPesan} - {self.idGuest.namaGuest}'
    
class DetailPemesanan(models.Model):
    idDetail = models.AutoField(primary_key=True)
    idPesan = models.ForeignKey(Pemesanan, verbose_name=_("Pemesanan"), on_delete=models.CASCADE)
    nomorKamar = models.ForeignKey(Kamar, verbose_name=_("Kamar"), on_delete=models.CASCADE)
    subTotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.nomorKamar and self.idPesan:
            self.subTotal = self.nomorKamar.idTipeKamar.hargaKamar * Decimal(self.idPesan.jumlah_hari)
            
        super().save(*args, **kwargs)

        pesanan = self.idPesan
        semua_detail = DetailPemesanan.objects.filter(idPesan=pesanan)
        total_harga_kamar = sum(d.subTotal for d in semua_detail if d.subTotal is not None)
        
        persen_diskon = 0
        if pesanan.idGuest.status.lower() == 'member' or pesanan.jumlah_hari >= 14:
            persen_diskon = pesanan.idGuest.idTipeGuest.persenDiskon
            if persen_diskon == 0:
                persen_diskon = 10
                
        nilai_diskon = total_harga_kamar * (Decimal(persen_diskon) / Decimal('100'))
        total_akhir = total_harga_kamar - nilai_diskon
        
        Pemesanan.objects.filter(pk=pesanan.pk).update(diskon=nilai_diskon, totalBayar=total_akhir)

    def delete(self, *args, **kwargs):
        pesanan = self.idPesan
        super().delete(*args, **kwargs)
        
        semua_detail = DetailPemesanan.objects.filter(idPesan=pesanan)
        total_harga_kamar = sum(d.subTotal for d in semua_detail if d.subTotal is not None)
        
        persen_diskon = 0
        if pesanan.idGuest.status.lower() == 'member' or pesanan.jumlah_hari >= 14:
            persen_diskon = pesanan.idGuest.idTipeGuest.persenDiskon
            if persen_diskon == 0:
                persen_diskon = 10
                
        nilai_diskon = total_harga_kamar * (Decimal(persen_diskon) / Decimal('100'))
        total_akhir = total_harga_kamar - nilai_diskon
        
        Pemesanan.objects.filter(pk=pesanan.pk).update(diskon=nilai_diskon, totalBayar=total_akhir)

    def __str__(self):
        return f'{self.idDetail} - {self.nomorKamar.idTipeKamar.namaTipekamar}'

class DetailPembayaran(models.Model):
    idDetailBayar = models.AutoField(primary_key=True)
    idPesan = models.ForeignKey(Pemesanan, verbose_name=_("Pemesanan"), on_delete=models.CASCADE)
    jumlahPembayaran = models.DecimalField(max_digits=12, decimal_places=2)
    buktiBayar = models.ImageField(upload_to='bukti_bayar/')

    def __str__(self):
        return f'Pembayaran {self.idDetailBayar} - Pesanan {self.idPesan.idPesan}'