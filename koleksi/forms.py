from django import forms

class CreateKategoriRambut(forms.Form):
    harga_jual = forms.IntegerField()
    tipe = forms.CharField()

class CreateKategoriMata(forms.Form):
    harga_jual = forms.IntegerField()
    warna = forms.CharField()

class CreateKategoriRumah(forms.Form):
    nama = forms.CharField()
    harga_jual = forms.IntegerField()
    harga_beli = forms.IntegerField()
    kapasitas_barang = forms.IntegerField()

class CreateKategoriBarang(forms.Form):
    nama = forms.CharField()
    harga_jual = forms.IntegerField()
    harga_beli = forms.IntegerField()
    tingkat_energi = forms.IntegerField()

class UpdateKategoriRambut(forms.Form):
    harga_jual = forms.IntegerField()
    tipe = forms.CharField()

class UpdateKategoriMata(forms.Form):
    harga_jual = forms.IntegerField()
    warna = forms.CharField()

class UpdateKategoriRumah(forms.Form):
    nama = forms.CharField()
    harga_jual = forms.IntegerField()
    harga_beli = forms.IntegerField()
    kapasitas_barang = forms.IntegerField()

class UpdateKategoriBarang(forms.Form):
    nama = forms.CharField()
    harga_jual = forms.IntegerField()
    harga_beli = forms.IntegerField()
    tingkat_energi = forms.IntegerField()