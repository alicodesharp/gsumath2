from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from gonderiler.forms import GirisForm, KayitForm, GonderiForm, DerslerForm, ProfilForm, AnnouncementsForm, changePassForm
from django.contrib.auth import authenticate, login, logout

from django.views.generic import TemplateView, RedirectView, FormView
from gonderiler.models import Gonderi, Ders, Egitmen, User, Announcements, Duyurular
from django.core.paginator import Paginator
# Create your views here.

class karsilama(TemplateView):
    template_name = 'karsilama.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("MYFLOW")
        return super(karsilama, self).dispatch(request,*args,**kwargs)

class MYFLOW(TemplateView):
    template_name = "myflow.html"
    def get_context_data(self, **kwargs):
        context = super(MYFLOW, self).get_context_data(**kwargs)
        sayfalanmis = Paginator(Gonderi.objects.all().order_by("-tarih"),5)  # bir üst satırdaki şeyin aynısını daha kolay yapıyor
        sayfa = self.request.GET.get("sayfa", 1)  # eğer sayfa diye birşey tanımlı değilse, 1 yani ilk sayfayı göster
        context['gonderiler'] = sayfalanmis.get_page(sayfa)
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        context["duyurucount"] = duyuru_adet
        return context




class kayit(FormView):
    template_name = 'kayit.html'
    form_class = KayitForm
    success_url = '/port/'
    def get_context_data(self, **kwargs):
        context = super(kayit, self).get_context_data(**kwargs)
        context['form'] = KayitForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super(kayit, self).dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        okul_no = form.cleaned_data['okul_no']
        if not User.objects.filter(username=username):
            if not User.objects.filter(okul_no=okul_no):
                user = User.objects.create(
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    email = form.cleaned_data['email'],
                    username = form.cleaned_data['username'],
                    okul_no = form.cleaned_data['okul_no']
                )
            else:
                errormsg = "Username or school number already exists, please pick another one."
                return render(self.request, "kayit.html", {
                    'error': errormsg,
                    'form': form
                })
            user.set_password('{}'.format(form.cleaned_data['password']))
            user.save()
            login(self.request,user)
            return super(kayit, self).form_valid(form)
        elif User.objects.filter(okul_no=okul_no):
            errormsg = "Username or school number already exists, please pick another one."
            return render(self.request, "kayit.html", {
                'error': errormsg,
                'form': form
            })
        else:
            errormsg = "Username or school number already exists, please pick another one."
            return render(self.request, "kayit.html", {
                'error': errormsg,
                'form': form
            })



class port(FormView):
    template_name = "port.html"
    form_class = DerslerForm
    success_url = "/akis_yonlendir/"
    def get_context_data(self, **kwargs):
        context=super(port, self).get_context_data(**kwargs)
        context["gonderiler"] = Gonderi.objects.all().order_by("-tarih")
        context["dersler"] = Ders.objects.all()
        context["egitmenler"] = Egitmen.objects.all();
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        context["duyurucount"] = duyuru_adet
        return context
    def form_valid(self, form):
        egitmen = form.cleaned_data['egitmen']
        ders_ad = form.cleaned_data['ders']
        gonderiler = Gonderi.objects.filter(egitmen=egitmen, ders=ders_ad).order_by("-tarih")
        return render(self.request, 'akis_goruntule.html',{
            'egitmen' : egitmen,
            'ders': ders_ad,
            'gonderiler': gonderiler,
        })
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/")
        return super(port, self).dispatch(request,*args,**kwargs)


class anasayfa(TemplateView):
    template_name = "anasayfa.html"
    def get_context_data(self, **kwargs):
        context = super(anasayfa, self).get_context_data(**kwargs)
        sayfalanmis = Paginator(Gonderi.objects.all().order_by("-tarih"), 5)  # bir üst satırdaki şeyin aynısını daha kolay yapıyor
        sayfa = self.request.GET.get("sayfa", 1)  # eğer sayfa diye birşey tanımlı değilse, 1 yani ilk sayfayı göster
        context['gonderiler'] = sayfalanmis.get_page(sayfa)
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        context["duyurucount"] = duyuru_adet
        return context  # eğer makale çok uzunsa ve bunu 1 sayfada değil de bölerek göstermek istiyorsak


class see_announcements(TemplateView):
    template_name = "Announcements.html"
    def get_context_data(self, **kwargs):
        context = super(see_announcements, self).get_context_data(**kwargs)
        sayfalanmis = Paginator(Duyurular.objects.all().order_by("-duyuru_tarih"),5)
        sayfa = self.request.GET.get("sayfa",1)
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        context["duyurucount"] = duyuru_adet
        context["duyurular"] = sayfalanmis.get_page(sayfa)
        return context


class giris(FormView):
    template_name = 'giris.html'
    form_class = GirisForm
    success_url = '/port/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super(giris, self).dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        user = authenticate(
           username = form.cleaned_data['username'],
           password = form.cleaned_data['password']
        )
        if user:
            login(self.request,user)
            return super(giris, self).form_valid(form)
        else:
            form = GirisForm()
            errormsg="Wrong password or username, please try again."
            return render(self.request,"giris.html",{
                'error':errormsg,
                'form':form
            })


class dersler(FormView):
    template_name = "dersler.html"
    form_class = ProfilForm
    def get_context_data(self, **kwargs):
        context = super(dersler, self).get_context_data(**kwargs)
        dersler2 = Ders.objects.all()
        context['form'] = DerslerForm()
        context['dersler'] = dersler2
        x = Duyurular.objects.all()
        duyuru_adet = x.count()
        context["duyurucount"] = duyuru_adet
        return context
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")
        return super(dersler, self).dispatch(request,*args,**kwargs)


def Takip(request,ders_id):
    ders = Ders.objects.get(id=ders_id)
    if ders in request.user.user.follows.all():
        request.user.user.follows.remove(ders)
    else:
        request.user.user.follows.add(ders)
    return redirect(request.META['HTTP_REFERER'])



class Send_Recommendation(FormView):
    template_name = "Oneri_gonder.html"
    form_class = AnnouncementsForm
    success_url = "/"
    def form_valid(self, form):
        baslik = form.cleaned_data["baslik"]
        text = form.cleaned_data["text"]
        gonderen_email = form.cleaned_data["gonderen_email"]
        Announcements.objects.create(
            baslik=baslik,
            text=text,
            gonderen_email=gonderen_email
        )
        return super(Send_Recommendation, self).form_valid(form)

class About_GsuMath(TemplateView):
    template_name = "about_gsumath.html"

class User_Profile(TemplateView):
    template_name = "user_profile.html"
    def get_context_data(self, **kwargs):
        context = super(User_Profile, self).get_context_data(**kwargs)
        context["follows"] = self.request.user.user.follows.all()
        return context

class Change_Your_Password(FormView):
    template_name = "changePass.html"
    form_class = changePassForm
    success_url = "/"
    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        if form.cleaned_data["new_password"] == form.cleaned_data["new_password_again"]:
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            return super(Change_Your_Password, self).form_valid(form)

        else:
            form = changePassForm()
            errormsg = "Passwords doesn't match."
            return render(self.request,"changePass.html",{
                "errormsg":errormsg,
                "form": form
            })







class yeni_paylasim(FormView):
    template_name = "yeni_paylasim.html"
    form_class = GonderiForm
    success_url = "/all_flow/"
    def get_context_data(self, **kwargs):
        context = super(yeni_paylasim, self).get_context_data(**kwargs)
        context["gonderiler"] = Gonderi.objects.all().order_by("-tarih")
        context["dersler"] = Ders.objects.all()
        context["egitmenler"] = Egitmen.objects.all();
        return context
    def form_valid(self, form):
        if "dosya" in self.request.FILES:
            Gonderi.objects.create(
                yazar = User.objects.get(id=self.request.user.id),
                konu = form.cleaned_data["konu"],
                text=form.cleaned_data["text"],
                dosya=self.request.FILES["dosya"],
                ders= form.cleaned_data["ders"],
                egitmen= form.cleaned_data["egitmen"]
            )

        else:
            Gonderi.objects.create(
                yazar= User.objects.get(id=self.request.user.id),
                konu=form.cleaned_data["konu"],
                text=form.cleaned_data["text"],
                ders=form.cleaned_data["ders"],
                egitmen = form.cleaned_data["egitmen"]
            )
        return super(yeni_paylasim, self).form_valid(form)


def ders_profil(request,id):
    ders = Ders.objects.filter(id=id)
    ders_turu = ""
    if ders[0].türü == "z":
        ders_turu="Mandatory"
    else:
        ders_turu="Optional"
    return render(request,"ders_profil.html", {
        'ders':ders[0],
        'ders_turu':ders_turu,
        'ders_id':ders[0].id,
        'count': Gonderi.objects.filter(ders=ders[0]).count()
    })

def gonderi_sil(request,gonderi_id):
    silinecek_oge = Gonderi.objects.filter(id=gonderi_id)
    silinecek_oge.delete()
    return redirect(request.META['HTTP_REFERER'])


class cikis(RedirectView):
    permanent = False
    pattern_name = "karsilama"
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(cikis, self).get_redirect_url(*args,**kwargs)


