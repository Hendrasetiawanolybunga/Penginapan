from django.contrib import admin
from .models import TipeKamar, Kamar
from core.admin import generate_action_buttons, format_rupiah

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