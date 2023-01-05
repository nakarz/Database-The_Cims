from django.shortcuts import render
from django.db import connection
from tools.tools import make_query
from django.http.response import HttpResponseRedirect, JsonResponse

LOGIN_URL = '/login'
APPAREL_LIST = '/use_apparel/list/'

def fetch_all_using_apparel(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            res = make_query(
                """
                select ma.username_pengguna, ma.nama_tokoh, ma.id_koleksi, kjb.nama, a.warna_apparel , a.nama_pekerjaan, a.kategori_apparel
                from menggunakan_apparel ma, apparel a, koleksi_jual_beli kjb
                where ma.ID_koleksi = a.ID_koleksi and a.ID_koleksi = kjb.ID_koleksi; 

                """
            )
    
        # data untuk pemain yang sedang login 
        else:
            uname_user = request.session['username']
            print(uname_user)
            res = make_query(
                f"""
                select ma.username_pengguna, ma.nama_tokoh, ma.id_koleksi, kjb.nama, a.warna_apparel , a.nama_pekerjaan, a.kategori_apparel
                from menggunakan_apparel ma, apparel a, koleksi_jual_beli kjb
                where ma.ID_koleksi = a.ID_koleksi and a.ID_koleksi = kjb.ID_koleksi and ma.username_pengguna = '{uname_user}';

                """
            )

        response = {
            'result' : res,
            'role': request.session['role']
        }
        
        print(res)
           
        return render(request, 'list_using_apparel.html', response)


    else:
        return HttpResponseRedirect(LOGIN_URL)

def delete_use_apparel(request, tokoh_name, id_koleksi):
    print("tokoh_name = " + tokoh_name)
    print("id_koleksi = " + id_koleksi)
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            uname_user = request.session['username']
            print(uname_user)
            make_query(
                f"""DELETE FROM menggunakan_apparel 
                WHERE username_pengguna = '{uname_user}' and nama_tokoh = '{tokoh_name}' and id_koleksi = '{id_koleksi}';
                """
            )
           
        return HttpResponseRedirect(APPAREL_LIST)


    else:
        return HttpResponseRedirect(LOGIN_URL)

def create_page(request):
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            uname_user = request.session['username']
            res = make_query(
                f"""
                select nama_tokoh 
                from koleksi_tokoh kt natural join apparel a 
                where a.id_koleksi = kt.id_koleksi and username_pengguna = '{uname_user}'
                group by nama_tokoh;
                """
            )

            return render(request, 'create_use_apparel.html', {'result' : res})
        
        return HttpResponseRedirect(APPAREL_LIST)

    else:
        return HttpResponseRedirect(LOGIN_URL)

def get_id_apparel(request):
    if request.method == 'GET':
        pilihan_tokoh = request.GET['pilihan_tokoh']
        print(pilihan_tokoh)
        uname_user = request.session['username']
        res = make_query(
            f"""
            select id_koleksi 
            from koleksi_tokoh kt natural join apparel a 
            where a.id_koleksi = kt.id_koleksi and username_pengguna = '{uname_user}' and nama_tokoh = '{pilihan_tokoh}';
            """
        )

        return JsonResponse({'result' : res})

def create_new_use_apparel(request):
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            if request.method == 'POST':
                uname_user = request.session['username']
                pilihan_tokoh = request.POST.get('pilihan_tokoh')
                pilihan_id_apparel = request.POST.get('pilihan_id_apparel')
                print("uname_user = " + uname_user)
                print("pilihan_tokoh = " + pilihan_tokoh)
                print("pilihan_id_apparel = " + pilihan_id_apparel)
                # CEK DULU DATANYA UDH ADA ATAU BELUM BIAR GA ERROR
                make_query(f"INSERT INTO MENGGUNAKAN_APPAREL VALUES ('{uname_user}', '{pilihan_tokoh}', '{pilihan_id_apparel}');")
        return HttpResponseRedirect(APPAREL_LIST)

    else:
        return HttpResponseRedirect(LOGIN_URL)
