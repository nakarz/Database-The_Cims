from collections import namedtuple
from django.shortcuts import render
from django.shortcuts import render
from django.db import connection
from koleksi.forms import *
from tools.tools import make_query, namedtuple_fetch_all
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def fetch_koleksi(request):
    if request.session.has_key('username'):
        res = make_query("SELECT * FROM KOLEKSI;")
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)
        return render(request, 'list_koleksi.html', response)
    else:
        return HttpResponseRedirect('/login')

# LIST (R)
# LIST APPAREL
def fetch_koleksi_list_apparel(request):
    if request.session.has_key('username'):
        res = make_query(""" 
            SELECT A.id_koleksi, KJB.nama, K.harga, KJB.harga_beli, A.kategori_apparel, A.nama_pekerjaan
            FROM KOLEKSI K, APPAREL A, KOLEKSI_JUAL_BELI KJB
            WHERE K.id = A.id_koleksi
            AND
            K.id = KJB.id_koleksi;        
            """)
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)
        return render(request, 'list/list_apparel.html', response)
    else:
        return HttpResponseRedirect('/login')

# LIST MATA
def fetch_koleksi_list_mata(request):
    if request.session.has_key('username'):
        res = make_query( 
            """
            SELECT M.id_koleksi, K.harga, M.warna
            FROM KOLEKSI AS K 
            NATURAL JOIN MATA AS M
            WHERE K.id = M.id_koleksi;
            """
            )
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)
        return render(request, 'list/list_mata.html', response)
    else:
        return HttpResponseRedirect('/login')

# LIST RAMBUT
def fetch_koleksi_list_rambut(request):
    if request.session.has_key('username'):
        res = make_query(
            """
            SELECT R.id_koleksi, K.harga, R.tipe
            FROM KOLEKSI AS K
            NATURAL JOIN RAMBUT AS R
            WHERE K.id = R.id_koleksi;
            """
            )
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)
        return render(request, 'list/list_rambut.html', response)
    else:
        return HttpResponseRedirect('/login')

# LIST RUMAH
def fetch_koleksi_list_rumah(request):
    if request.session.has_key('username'):
        res = make_query(
            """
            SELECT R.id_koleksi, KJB.nama, K.harga, KJB.harga_beli, R.kapasitas_barang
            FROM KOLEKSI K, RUMAH R, KOLEKSI_JUAL_BELI KJB
            WHERE K.id = R.id_koleksi
            AND
            K.id = KJB.id_koleksi;
            """)
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)
        return render(request, 'list/list_rumah.html', response)
    else:
        return HttpResponseRedirect('/login')

# LIST BARANG
def fetch_koleksi_list_barang(request):
    if request.session.has_key('username'):
        res = make_query(
            """
            SELECT B.id_koleksi, KJB.nama, K.harga, KJB.harga_beli, B.tingkat_energi
            FROM KOLEKSI K, BARANG B, KOLEKSI_JUAL_BELI KJB
            WHERE K.id = B.id_koleksi
            AND
            K.id = KJB.id_koleksi;
            """)
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)
        return render(request, 'list/list_barang.html', response)
    else:
        return HttpResponseRedirect('/login')

# CREATE KOLEKSI PAGE
def create_koleksi(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'create_koleksi.html')

        return HttpResponseRedirect('/koleksi/create/')
    else:
        return HttpResponseRedirect('/login')  

# FORM (C)
# FORM RAMBUT 
# def namedtuplefetchall(cursor):
#     "Return all rows from a cursor as a namedtuple"
#     desc = cursor.description
#     nt_result = namedtuple('Result', [col[0] for col in desc])
#     return [nt_result(*row) for row in cursor.fetchall()]
    
# @csrf_exempt
# def create_koleksi_rambut(request):
#     cursor = connection.cursor()
#     cursor.execute("SET SEARCH_PATH TO THECIMS")
#     cursor.execute("SELECT MAX(id_koleksi) FROM RAMBUT")

#     res = namedtuplefetchall(cursor)
#     for i in res:
#         id = i 
#     id_numb = int(id[0][2:5]) + 1
#     id_numb_convert = str(id_numb)

#     create_kategori_rambut_form = CreateKategoriRambut(request.POST)
#     if(request.method == 'POST'):
#         if(create_kategori_rambut_form.is_valid()):
#             id_baru = 'RB' + id_numb_convert.zfill(3)
#             harga_jual = create_kategori_rambut_form.cleaned_data['harga_jual']
#             tipe = create_kategori_rambut_form['tipe']

#             cursor.execute("SET SEARCH_PATH TO THECIMS")
#             cursor.execute("INSERT INTO KOLEKSI (id, harga) VALUES(%s, %s);", [id_baru, harga_jual])
#             cursor.execute("INSERT INTO RAMBUT (id_koleksi, tipe) VALUES(%s, %s);", [id_baru, tipe])
#             return HttpResponseRedirect('/koleksi/form/form_rambut/')
    
#     return render(request, 'form/form_rambut.html', {'form':create_kategori_rambut_form, 'id':id_numb_convert.zfill(3)})

# FORM RAMBUT
def create_koleksi_rambut(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'form/form_rambut.html')
        return HttpResponseRedirect('form/form_rambut/')
    else:
        return HttpResponseRedirect('/login')  

def create_new_koleksi_rambut(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                # new_id = request.POST.get('new_id')
                new_harga_jual = request.POST.get('new_harga_jual')
                new_tipe_rambut = request.POST.get('new_tipe_rambut')
                # print("new id = " + new_id)
                print("new harga jual= " + new_harga_jual)
                print("new tipe rambut = " + new_tipe_rambut)
                make_query(f"INSERT INTO RAMBUT VALUES ('{new_harga_jual}', '{new_tipe_rambut}');")
                return HttpResponseRedirect('/koleksi/list/list_rambut/')
        return render(request, 'form/form_rambut.html')  
    else:
        return HttpResponseRedirect('/login')


# FORM MATA
def create_koleksi_mata(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'form/form_mata.html')

        return HttpResponseRedirect('/koleksi/create/')
    else:
        return HttpResponseRedirect('/login') 

def create_new_koleksi_mata(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                # new_id = request.POST.get('new_id')
                new_harga_jual = request.POST.get('new_harga_jual')
                new_warna_mata = request.POST.get('new_warna_mata')
                # print("new id = " + new_id)
                print("new harga jual= " + new_harga_jual)
                print("new warna mata = " + new_warna_mata)
                make_query(f"INSERT INTO MATA VALUES ('{new_harga_jual}', '{new_warna_mata}');")
                return HttpResponseRedirect('/koleksi/list/list_mata/')
        return render(request, 'form/form_mata.html')  
    else:
        return HttpResponseRedirect('/login')

# FORM RUMAH
def create_koleksi_rumah(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'form/form_rumah.html')

        return HttpResponseRedirect('/koleksi/create/')
    else:
        return HttpResponseRedirect('/login')  

def create_new_koleksi_rumah(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                # new_id = request.POST.get('new_id')
                new_nama_rumah = request.POST.get('new_nama_rumah')
                new_harga_jual = request.POST.get('new_harga_jual')
                new_kapasitas_barang = request.POST.get('new_kapasitas_barang')
                # print("new id = " + new_id)
                print("new_nama_rumah = " + new_nama_rumah)
                print("new harga jual= " + new_harga_jual)
                print("new warna mata = " + new_kapasitas_barang)
                make_query(f"INSERT INTO RUMAH VALUES ('{new_nama_rumah}', '{new_harga_jual}', '{new_kapasitas_barang}');")
                return HttpResponseRedirect('/koleksi/list/list_rumah/')
        return render(request, 'form/form_rumah.html')  
    else:
        return HttpResponseRedirect('/login')

# FORM BARANG
def create_koleksi_barang(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'form/form_barang.html')

        return HttpResponseRedirect('/koleksi/create/')
    else:
        return HttpResponseRedirect('/login')  

def create_new_koleksi_barang(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                # new_id = request.POST.get('new_id')
                new_nama_rumah = request.POST.get('new_nama_barang')
                new_harga_jual = request.POST.get('new_harga_jual')
                new_harga_beli = request.POST.get('new_harga_beli')
                new_tingkat_energi = request.POST.get('new_tingkat_energi')
                # print("new id = " + new_id)
                print("new_nama_rumah = " + new_nama_rumah)
                print("new harga jual= " + new_harga_jual)
                print("new harga beli = " + new_harga_beli)
                print("new tingkat energi = " + new_tingkat_energi)
                make_query(f"INSERT INTO BARANG VALUES ('{new_nama_rumah}', '{new_harga_jual}', '{new_harga_beli}', '{new_tingkat_energi}');")
                return HttpResponseRedirect('/koleksi/list/list_barang/')
        return render(request, 'form/form_barang.html')  
    else:
        return HttpResponseRedirect('/login')

def create_koleksi_apparel(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'form/form_apparel.html')

        return HttpResponseRedirect('/koleksi/create/')
    else:
        return HttpResponseRedirect('/login')  

def create_new_koleksi_apparel(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                # new_id = request.POST.get('new_id')
                new_nama_apparel = request.POST.get('new_nama_apparel')
                new_harga_jual = request.POST.get('new_harga_jual')
                new_harga_beli = request.POST.get('new_harga_beli')
                new_warna_apparel = request.POST.get('new_warna_apparel')
                # print("new id = " + new_id)
                print("new warna apparel = " + new_nama_apparel)
                print("new harga jual= " + new_harga_jual)
                print("new harga beli = " + new_harga_beli)
                print("new warna apparel = " + new_warna_apparel)
                make_query(f"INSERT INTO APPAREL VALUES ('{new_nama_apparel}', '{new_harga_jual}', '{new_harga_beli}', '{new_warna_apparel}');")
                return HttpResponseRedirect('/koleksi/list/list_apparel/')
        return render(request, 'form/form_apparel.html')  
    else:
        return HttpResponseRedirect('/login')

# def create_new_koleksi(request):
#     if request.session.has_key('username'):
#         if request.session['role'] != 'admin':
#             if request.method == 'POST':
#                 uname_user = request.session['username']
#                 pilihan_tokoh = request.POST.get('pilihan_tokoh')
#                 pilihan_id_koleksi = request.POST.get('pilihan_id_koleksi')
#                 print("uname_user = " + uname_user)
#                 print("pilihan_tokoh = " + pilihan_tokoh)
#                 print("pilihan_id_koleksi = " + pilihan_id_koleksi)
#         return HttpResponseRedirect('/koleksi_tokoh/list/')
#     else:
#         return HttpResponseRedirect('/login')

def update_koleksi(request, koleksi):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            print("koleksi = " + koleksi)
            res = make_query(f"SELECT * FROM KOLEKSI WHERE KOLEKSI = {koleksi};")
            print(res[0])
            return render(request, 'update_level.html', {'result' : res[0]})
        else:
            return HttpResponseRedirect('/koleksi/list/')
    else:
        return HttpResponseRedirect('/login')

def delete_koleksi(request, koleksi):
    print("koleksi = " + koleksi)
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            uname_user = request.session['username']
            print(uname_user)
            res = make_query("SELECT * FROM KOLEKSI;")
        return HttpResponseRedirect('/koleksi/list/')
    else:
        return HttpResponseRedirect('/login')

def update_rambut_admin(request, id, harga, tipe):
    print(id)
    cursor = connection.cursor()

    update_rambut_form = CreateKategoriBarang(request.POST)
    if (request.method == 'POST'):
        if (update_rambut_form.is_valid()):
            cursor.execute("SET SEARCH_PATH TO THECIMS")
            harga_jual = update_rambut_form.cleaned_data['harga_jual']
            tipe = update_rambut_form.cleaned_data['tipe']

            cursor.execute("UPDATE KOLEKSI SET HARGA = %s WHERE id = %s;", [harga_jual, id])
            cursor.execute("UPDATE RAMBUT SET TIPE = %s WHERE id_koleksi = %s ", [tipe, id])
            return HttpResponseRedirect('/koleksi/update_rambut_admin')

    return render(request, 'update_rambut.html', {'form': update_rambut_form, 'id':id, 'harga_jual':harga, 'tipe':tipe})

def update_mata_admin(request, id, harga, warna):
    print(id)
    cursor = connection.cursor()

    update_mata_form = CreateKategoriMata(request.POST)
    if (request.method == 'POST'):
        if (update_mata_form.is_valid()):
            cursor.execute("SET SEARCH_PATH TO THECIMS")
            harga_jual = update_mata_form.cleaned_data['harga_jual']
            warna = update_mata_form.cleaned_data['warna']

            cursor.execute("UPDATE KOLEKSI SET HARGA = %s WHERE id = %s;", [harga_jual, id])
            cursor.execute("UPDATE MATA SET WARNA = %s WHERE id_koleksi = %s ", [warna, id])
            return HttpResponseRedirect('/koleksi/update_mata_admin')

    return render(request, 'update_mata.html', {'form': update_mata_form, 'id':id, 'harga_jual':harga, 'warna':warna})

def update_rumah_admin(request, id, nama, harga, harga_beli, kapasitas_barang):
    print(id)
    cursor = connection.cursor()

    update_rumah_form = CreateKategoriRumah(request.POST)
    if (request.method == 'POST'):
        if (update_rumah_form.is_valid()):
            cursor.execute("SET SEARCH_PATH TO THECIMS")
            nama = update_rumah_form.cleaned_data['nama']
            harga_jual = update_rumah_form.cleaned_data['harga_jual']
            harga_beli = update_rumah_form.cleaned_data['harga_beli']
            kapasitas_barang = update_rumah_form.cleaned_data['kapasitas_barang']

            cursor.execute("UPDATE KOLEKSI SET HARGA = %s WHERE id = %s;", [harga_jual, id])
            cursor.execute("UPDATE KOLEKSI_JUAL_BELI SET NAMA = %s, HARGA_BELI = %s WHERE id_koleksi = %s ", [nama, harga_beli, id])
            cursor.execute("UPDATE RUMAH SET KAPASITAS_BARANG = %s WHERE ID_KOLEKSI = %s", [kapasitas_barang, id])
            return HttpResponseRedirect('/koleksi/update_rumah_admin')

    return render(request, 'update_rumah.html', {'form': update_rumah_form, 'id':id, 'nama':nama, 'harga_jual':harga, 'harga_beli':harga_beli, 'kapasitas_barang':kapasitas_barang})


def update_barang_admin(request, id, nama, harga, harga_beli, tingkat_energi):
    print(id)
    cursor = connection.cursor()

    update_barang_form = CreateKategoriBarang(request.POST)
    if (request.method == 'POST'):
        if (update_barang_form.is_valid()):
            cursor.execute("SET SEARCH_PATH TO THECIMS")
            nama = update_barang_form.cleaned_data['nama']
            harga_jual = update_barang_form.cleaned_data['harga_jual']
            harga_beli = update_barang_form.cleaned_data['harga_beli']
            tingkat_energi = update_barang_form.cleaned_data['tingkat_energi']

            cursor.execute("UPDATE KOLEKSI SET HARGA = %s WHERE id = %s;", [harga_jual, id])
            cursor.execute("UPDATE KOLEKSI_JUAL_BELI SET NAMA = %s, HARGA_BELI = %s WHERE id_koleksi = %s ", [nama, harga_beli, id])
            cursor.execute("UPDATE BARANG SET TINGKAT_ENERGI = %s WHERE ID_KOLEKSI = %s", [tingkat_energi, id])
            return HttpResponseRedirect('/koleksi/update_barang_admin')

    return render(request, 'update_barang.html', {'form': update_barang_form, 'id':id, 'nama':nama, 'harga_jual':harga, 'harga_beli':harga_beli, 'tingkat_energi':tingkat_energi})

def delete_rambut_admin(request, pk):
    print(pk)
    cursor = connection.cursor()

    cursor.execute("SET SEARCH_PATH TO THECIMS")
    cursor.execute("DELETE FROM KOLEKSI WHERE id = %s", [pk])
    return HttpResponseRedirect('/koleksi/delete_rambut_admin')

def delete_mata_admin(request, pk):
    print(pk)
    cursor = connection.cursor()

    cursor.execute("SET SEARCH_PATH TO THECIMS")
    cursor.execute("DELETE FROM KOLEKSI WHERE id = %s", [pk])
    return HttpResponseRedirect('/koleksi/delete_mata_admin')

def delete_rumah_admin(request, pk):
    print(pk)
    cursor = connection.cursor()

    cursor.execute("SET SEARCH_PATH TO THECIMS")
    cursor.execute("DELETE FROM KOLEKSI WHERE id = %s", [pk])
    return HttpResponseRedirect('/koleksi/delete_rumah_admin')

def delete_barang_admin(request, pk):
    print(pk)
    cursor = connection.cursor()

    cursor.execute("SET SEARCH_PATH TO THECIMS")
    cursor.execute("DELETE FROM KOLEKSI WHERE id = %s", [pk])
    return HttpResponseRedirect('/koleksi/delete_barang_admin')