from django import forms
from gonderiler.models import Ders, Gonderi, Egitmen

class GirisForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class GonderiForm(forms.Form):
    konu = forms.CharField(max_length=50)
    text = forms.CharField(max_length=10000)
    dosya = forms.FileField(required=False)
    ders = forms.ModelChoiceField(
        queryset= Ders.objects.all(),
        label="ders"
    )
    egitmen= forms.ModelChoiceField(
        queryset=Egitmen.objects.all(),
        label="egitmen"
    )

class changePassForm(forms.Form):
    new_password = forms.CharField(max_length=20)
    new_password_again = forms.CharField(max_length=20)

class ProfilForm(forms.Form):
    pass


class KayitForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    okul_no = forms.IntegerField(max_value=99999999, min_value=10000000, label="School number")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class DerslerForm(forms.Form):
    ders = forms.ModelChoiceField(
        queryset=Ders.objects.all(),
        label="ders"
    )
    egitmen = forms.ModelChoiceField(
        queryset=(Egitmen.objects.all()),
        label="egitmen"
    )

class AnnouncementsForm(forms.Form):
    baslik = forms.CharField(max_length=50, label="Subject: ")
    text = forms.CharField(max_length=1000, label="Your message: ")
    gonderen_email = forms.CharField(max_length=100, label="Your e-mail adress: ")
