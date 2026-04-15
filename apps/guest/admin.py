from django.contrib import admin
from .models import TipeGuest, Guest
from core.admin import generate_action_buttons

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