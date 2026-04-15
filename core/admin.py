from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import TipeKamar, Kamar, TipeGuest, Guest, Pemesanan, DetailPemesanan, DetailPembayaran

admin.site.site_header = "Sistem Manajemen Penginapan" 
admin.site.site_title = "Admin HMS"                     
admin.site.index_title = "Panel Kontrol Utama"

def generate_action_buttons(obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.model_name
    edit_url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
    delete_url = reverse(f"admin:{app_label}_{model_name}_delete", args=[obj.pk])
    return format_html(
        '<a class="button" href="{}" style="background-color:#417690; color:white; padding:4px 8px; border-radius:4px; text-decoration:none; margin-right:5px;">Edit</a>'
        '<a class="button" href="{}" style="background-color:#ba2121; color:white; padding:4px 8px; border-radius:4px; text-decoration:none;">Hapus</a>',
        edit_url, delete_url
    )
generate_action_buttons.short_description = 'Aksi'

def format_rupiah(value):
    if value is not None:
        return f"Rp {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "Rp 0,00"

@admin.register(TipeKamar)
class TipeKamarAdmin(admin.ModelAdmin):
    list_display = ('namaTipekamar', 'harga_kamar_rp', 'get_aksi')
    search_fields = ('namaTipekamar',)

    def harga_kamar_rp(self, obj):
        return format_rupiah(obj.hargaKamar)
    harga_kamar_rp.short_description = 'Harga Kamar'

    def get_aksi(self, obj):
        return generate_action_buttons(obj)
    get_aksi.short_description = 'Aksi'

@admin.register(Kamar)
class KamarAdmin(admin.ModelAdmin):
    list_display = ('nomorKamar', 'idTipeKamar', 'posisiLantai', 'statusKamar', 'get_aksi')
    list_display_links = ('nomorKamar',)
    list_filter = ('statusKamar', 'posisiLantai', 'idTipeKamar')
    search_fields = ('keteranganKondisi',)

    def get_aksi(self, obj):
        return generate_action_buttons(obj)
    get_aksi.short_description = 'Aksi'

@admin.register(TipeGuest)
class TipeGuestAdmin(admin.ModelAdmin):
    list_display = ('namaTipeGuest', 'persenDiskon', 'get_aksi')
    
    def get_aksi(self, obj):
        return generate_action_buttons(obj)
    get_aksi.short_description = 'Aksi'

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('namaGuest', 'status', 'nomorTelepon', 'idTipeGuest', 'get_aksi')
    list_filter = ('status', 'idTipeGuest')
    search_fields = ('namaGuest', 'nomorTelepon')

    def get_aksi(self, obj):
        return generate_action_buttons(obj)
    get_aksi.short_description = 'Aksi'

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