"""e11_cims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from white import urls as white
from purple_misi_utama import urls as misi_utama
from purple_makanan import urls as makanan
from warna_kulit import urls as warna_kulit
from level import urls as level
from menggunakan_apparel import urls as use_apparel
from pekerjaan import urls as pekerjaan
from menggunakan_barang import urls as use_item
from bekerja import urls as bekerja
from kategori_apparel import urls as kategori_apparel
from koleksi import urls as koleksi
from koleksi_tokoh import urls as koleksi_tokoh


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(white)),
    path('main-mission/', include(misi_utama)),
    path('foods/', include(makanan)),
    path('warna_kulit/', include(warna_kulit)),
    path('level/', include(level)),
    path('use_apparel/', include(use_apparel)),
    path('job/', include (pekerjaan)),
    path('use_item/', include(use_item)),
    path('bekerja/', include(bekerja)),
    path('kategori_apparel/', include(kategori_apparel)),
    path('koleksi_tokoh/', include(koleksi_tokoh)),
    path('koleksi/', include (koleksi)),
]
