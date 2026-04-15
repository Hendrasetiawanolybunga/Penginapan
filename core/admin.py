from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

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