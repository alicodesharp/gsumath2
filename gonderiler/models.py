from django.db import models
from django.contrib.auth.models import User as AsilUser

türler = [('z', 'Zorunlu'), ('s', 'Seçmeli')]
# Create your models here.

class Egitmen(models.Model):
    unvan_ve_isim = models.CharField(max_length=100)
    isim = models.CharField(max_length=50)
    soyisim = models.CharField(max_length=50)
    unvan = models.CharField(max_length=50, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Eğitmenler"
    def __str__(self):
        return self.isim



class Ders(models.Model):
    name = models.CharField(max_length=50)
    derskodu = models.CharField(max_length=20)
    yariyil = models.IntegerField()
    türü = models.CharField(choices=türler, max_length=20)
    ders_text = models.TextField(default="Ders")
    class Meta:
        verbose_name_plural = "Dersler"
    def __str__(self):
        return self.name


class User(AsilUser):
    follows = models.ManyToManyField(Ders,related_name="followed_by")
    okul_no = models.IntegerField(unique=True)



class Gonderi(models.Model):
    yazar = models.ForeignKey(User, on_delete=models.CASCADE)
    konu = models.CharField(max_length=50)
    text = models.TextField()
    dosya = models.FileField(upload_to="files", null=True, blank=True)
    tarih = models.DateTimeField(auto_now_add=True)
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    egitmen = models.ForeignKey(Egitmen, on_delete=models.CASCADE)


class Announcements(models.Model):
    baslik = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    gonderen_email = models.CharField(max_length=50)
    gonderi_tarih = models.DateTimeField(auto_now_add=True)

class Duyurular(models.Model):
    baslik = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    duyuru_tarih = models.DateTimeField(auto_now_add=True)

