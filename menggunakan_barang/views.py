from datetime import *
from django.shortcuts import render
from tools.tools import make_query
from django.http.response import HttpResponseRedirect


def tampilkan_using_item(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            res = make_query(
                """
                select mb.username_pengguna, mb.nama_tokoh, mb.waktu, kjb.nama
                from menggunakan_barang mb, barang b, koleksi_jual_beli kjb
                where mb.ID_barang = b.ID_koleksi and b.ID_koleksi = kjb.ID_koleksi
                order by mb.username_pengguna asc;
                """)

        else:
            uname_user = request.session['username']
            print(uname_user)
            res = make_query(
                f"""
                select mb.nama_tokoh, mb.waktu, kjb.nama
                from menggunakan_barang mb, barang b, koleksi_jual_beli kjb
                where mb.ID_barang = b.ID_koleksi and b.ID_koleksi = kjb.ID_koleksi and mb.username_pengguna = '{uname_user}'
                order by mb.nama_tokoh asc;
                """)

        response = {
            'result' : res,
            'role': request.session['role']
        }

        print(res)
        return render(request, 'list_using_item.html', response)

    else:
        return HttpResponseRedirect('/login')



def create_using_item(request):
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            uname_user = request.session['username']
            tokoh = make_query(f" select nama from tokoh where username_pengguna = '{uname_user}';")
            item = make_query(f"""
                select distinct b.id_koleksi 
                from koleksi_tokoh k, barang b 
                where k.id_koleksi = b.id_koleksi and k.username_pengguna = '{uname_user}';""")

            return render(request, 'create_use_item.html', {'tokoh' : tokoh, 'item' : item})
        return HttpResponseRedirect('/use_item/list/')

    else:
        return HttpResponseRedirect('/login')



def create_new_use_item(request):
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            if request.method == 'POST':

                uname_user = request.session['username']
                pilihan_tokoh = request.POST.get('pilihan_tokoh')
                pilihan_item = request.POST.get('pilihan_item')

                print("uname_user = " + uname_user)
                print("pilihan_tokoh = " + pilihan_tokoh)
                print("pilihan_id_item = " + pilihan_item)

                energi_tokoh = make_query(f"select energi from tokoh where username_pengguna = '{uname_user}' and nama = '{pilihan_tokoh}';")
                energi_min = make_query(f"select tingkat_energi from barang where id_koleksi = '{pilihan_item}';")

                if energi_tokoh[0][0] >= energi_min[0][0]:
                    current_datetime = datetime.now()
                    make_query(f"INSERT INTO MENGGUNAKAN_BARANG VALUES ('{uname_user}', '{pilihan_tokoh}', '{current_datetime}', '{pilihan_item}');")
                
                else:
                    tokoh = make_query(f" select nama from tokoh where username_pengguna = '{uname_user}';")
                    item = make_query(f"""
                        select distinct k.id_koleksi from koleksi_tokoh k, barang b 
                        where k.id_koleksi = b.id_koleksi and k.username_pengguna = '{uname_user}';""")

                    return render(request, 'create_use_item.html', {
                        'tokoh' : tokoh, 
                        'item' : item,
                        'error': "Energi tokoh tidak mencukupi sehingga barang tidak dapat digunakan."})

        return HttpResponseRedirect('/use_item/list/')

    else:
        return HttpResponseRedirect('/login')