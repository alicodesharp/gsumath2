"""gsumathss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from gonderiler.views import karsilama, kayit, giris, cikis, port, yeni_paylasim, anasayfa, gonderi_sil, ders_profil, dersler, Send_Recommendation, see_announcements, About_GsuMath, User_Profile, Change_Your_Password, Takip, MYFLOW
urlpatterns = [
    path('', karsilama.as_view(), name='karsilama'),
    path('all_flow/', anasayfa.as_view(), name="anasayfa"),
    path('myflow/', MYFLOW.as_view(), name="MYFLOW"),
    path('user_profile/', User_Profile.as_view()),
    path('gonderi_sil/<int:gonderi_id>', gonderi_sil),
    path('course_profile/<int:id>', ders_profil),
    path('kayit/', kayit.as_view(), name='kayıt'),
    path('giris/', giris.as_view(), name='giris'),
    path('courses_list/', dersler.as_view(), name='dersler'),
    path('yeni_paylasim/', yeni_paylasim.as_view(), name="yeni paylasim"),
    path('announcements/', see_announcements.as_view()),
    path('cikis/', cikis.as_view(), name='cikis'),
    path('port/', port.as_view(),name="yonlendirme"),
    path('send_recommendation/', Send_Recommendation.as_view()),
    path('about_gsumath/',About_GsuMath.as_view()),
    path('change_password/',Change_Your_Password.as_view()),
    path('follow/<int:ders_id>', Takip),
    path('-adminsec-/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
