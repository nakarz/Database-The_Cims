from django.shortcuts import render
from django.db import connection
from tools.tools import make_query
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def fetch_koleksi_tokoh(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            res = make_query(
                """
                SELECT KT.username_pengguna, KT.nama_tokoh, KT.id_koleksi
                FROM KOLEKSI_TOKOH KT
                """
            )
    
        # data untuk pemain yang sedang login (show miliknya)
        else:
            uname_user = request.session['username']
            print(uname_user)
            res = make_query(
                f"""
                SELECT KT.username_pengguna, KT.nama_tokoh, KJB.id_koleksi
                FROM KOLEKSI_TOKOH KT, KOLEKSI_JUAL_BELI KJB, KOLEKSI K
                WHERE KT.id_koleksi = K.id
                AND
                K.id = KJB.id_koleksi
                AND
                KT.username_pengguna = '{uname_user}';
                """
            )
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)
        return render(request, 'list_koleksi_tokoh.html', response)
    else:
        return HttpResponseRedirect('/login')

def create_koleksi_tokoh(request):
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            uname_user = request.session['username']
            res1 = make_query(
                f"""
                SELECT T.nama
                FROM PEMAIN P, TOKOH T 
                WHERE P.username = T.username_pengguna
                AND
                T.username_pengguna='{uname_user}'
            """)
            res2 = make_query(
                f"""
                SELECT id FROM KOLEKSI
                """
            )
            return render(request, 'create_koleksi_tokoh.html', {'result1' : res1, 'result2': res2})
        return HttpResponseRedirect('/koleksi_tokoh/list/')
    else:
        return HttpResponseRedirect('/login')

def create_new_koleksi_tokoh(request):
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            if request.method == 'POST':
                uname_user = request.session['username']
                pilihan_tokoh = request.POST.get('pilihan_tokoh')
                pilihan_id_koleksi = request.POST.get('pilihan_id_koleksi')
                print("uname_user = " + uname_user)
                print("pilihan_tokoh = " + pilihan_tokoh)
                print("pilihan_id_koleksi = " + pilihan_id_koleksi)
                make_query(f"INSERT INTO KOLEKSI_TOKOH VALUES ('{pilihan_id_koleksi}', '{uname_user}', '{pilihan_tokoh}');")
            return HttpResponseRedirect('/koleksi_tokoh/list/') 
    else:
        return HttpResponseRedirect('/login')

# def get_id_koleksi_tokoh(request):
#     if request.method == 'GET':
#         pilihan_tokoh = request.GET['pilihan_tokoh']
#         print(pilihan_tokoh)
#         uname_user = request.session['username']
#         res = make_query(
#             f"""
#             SELECT id_koleksi 
#             FROM KOLEKSI_TOKOH KT NATURAL JOIN KOLEKSI K
#             WHERE K.id = KT.id_koleksi 
#             AND
#             KT.username_pengguna = '{uname_user}' 
#             AND
#             KT.nama_tokoh = '{pilihan_tokoh}';
#             """
#         )
#         return JsonResponse({'result' : res})

def delete_koleksi_tokoh(request, tokoh):
    namaTokoh = '' + tokoh
    print("tokoh = " + tokoh)
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
           make_query(
               f"DELETE FROM KOLEKSI_TOKOH WHERE nama_tokoh = '{namaTokoh}'"
           )
        return HttpResponseRedirect('/koleksi_tokoh/list/')
    else:
        return HttpResponseRedirect('/login')