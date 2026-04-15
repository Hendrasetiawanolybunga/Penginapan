from django.contrib import admin
from .models import TipeKamar, Kamar, TipeGuest, Guest, Pemesanan, DetailPemesanan, DetailPembayaran


admin.site.site_header = "Sistem Manajemen Penginapan" 
admin.site.site_title = "Admin HMS"                     
admin.site.index_title = "Panel Kontrol Utama"


@admin.register(TipeKamar)
class TipeKamarAdmin(admin.ModelAdmin):
    list_display = ('idtipekamar', 'namaTipekamar', 'hargaKamar')
    list_display_links = ('idtipekamar', 'namaTipekamar')
    search_fields = ('namaTipekamar',)

@admin.register(Kamar)
class KamarAdmin(admin.ModelAdmin):
    list_display = ('nomorKamar', 'idTipeKamar', 'posisiLantai', 'statusKamar')
    list_display_links = ('nomorKamar',)
    list_filter = ('statusKamar', 'posisiLantai', 'idTipeKamar')
    search_fields = ('keteranganKondisi',)

@admin.register(TipeGuest)
class TipeGuestAdmin(admin.ModelAdmin):
    list_display = ('idTipeGuest', 'namaTipeGuest', 'persenDiskon')
    list_display_links = ('idTipeGuest', 'namaTipeGuest')

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('idGuest', 'namaGuest', 'status', 'nomorTelepon', 'idTipeGuest')
    list_display_links = ('idGuest', 'namaGuest')
    list_filter = ('status', 'idTipeGuest')
    search_fields = ('namaGuest', 'nomorTelepon')

class DetailPemesananInline(admin.TabularInline):
    model = DetailPemesanan
    extra = 1

class DetailPembayaranInline(admin.TabularInline):
    model = DetailPembayaran
    extra = 1

@admin.register(Pemesanan)
class PemesananAdmin(admin.ModelAdmin):
    list_display = ('idPesan', 'idGuest', 'tanggalPesan', 'tanggalCheckin', 'statusPembayaran', 'totalBayar')
    list_display_links = ('idPesan', 'idGuest')
    list_filter = ('statusPembayaran', 'metodeBayar', 'tanggalPesan')
    search_fields = ('idGuest__namaGuest',)
    inlines = [DetailPemesananInline, DetailPembayaranInline]