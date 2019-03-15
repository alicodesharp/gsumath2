from django.contrib import admin
from gonderiler.models import Gonderi, Ders, türler, Egitmen, User, Announcements, Duyurular

unvans = [('u', Egitmen.unvan,Egitmen.isim,Egitmen.soyisim)]

def zorunlu_ders(Ders, request, türler):
    türler.update(türü='z')

zorunlu_ders.short_description = "Zorunlu ders yap"




class DersAdmin(admin.ModelAdmin):
    list_display = ['name', 'derskodu', 'yariyil', 'türü','ders_text']
    list_filter = ['yariyil', 'türü']
    actions = [zorunlu_ders]

class GonderiAdmin(admin.ModelAdmin):
    list_display = ['yazar', 'text', 'tarih', 'konu']
    list_filter = ['yazar', 'tarih']

class EgitmenAdmin(admin.ModelAdmin):
    list_display = ['isim', 'soyisim', 'unvan','unvan_ve_isim']
    list_filter = ['isim']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name' ,'last_name','email']

class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ["baslik","text","gonderen_email"]

class DuyurularAdmin(admin.ModelAdmin):
    list_display = ["baslik","text","duyuru_tarih"]




admin.site.register(User, UserAdmin)
admin.site.register(Ders, DersAdmin)
admin.site.register(Gonderi,GonderiAdmin)
admin.site.register(Announcements,AnnouncementsAdmin)
admin.site.register(Duyurular,DuyurularAdmin)
admin.site.register(Egitmen,EgitmenAdmin)
