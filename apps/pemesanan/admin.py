from django.contrib import admin
from .models import Pemesanan, DetailPemesanan
from apps.pembayaran.models import DetailPembayaran
from core.admin import generate_action_buttons, format_rupiah

class DetailPemesananInline(admin.TabularInline):
    model = DetailPemesanan
    extra = 1
    readonly_fields = ('subTotal',)

class DetailPembayaranInline(admin.TabularInline):
    model = DetailPembayaran
    extra = 1

@admin.register(Pemesanan)
class PemesananAdmin(admin.ModelAdmin):
    list_display = ('idGuest', 'tanggalPesan', 'tanggalCheckin', 'durasi_nginap', 'statusPembayaran', 'total_bayar_rp', 'get_aksi')
    list_filter = ('statusPembayaran', 'metodeBayar', 'tanggalPesan')
    search_fields = ('idGuest__namaGuest',)
    inlines = [DetailPemesananInline, DetailPembayaranInline]
    readonly_fields = ('diskon', 'totalBayar')

    def durasi_nginap(self, obj):
        return f"{obj.jumlah_hari} Hari"
    durasi_nginap.short_description = 'Durasi Nginap'

    def total_bayar_rp(self, obj):
        return format_rupiah(obj.totalBayar)
    total_bayar_rp.short_description = 'Total Bayar'

    def get_aksi(self, obj):
        return generate_action_buttons(obj)
    get_aksi.short_description = 'Aksi'