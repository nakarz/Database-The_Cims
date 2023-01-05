import re
from django.shortcuts import render
from django.db import connection
from tools.tools import make_query
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def fetch_kategori_apparel(request):
    if request.session.has_key('username'):
        res = make_query("""
        SELECT nama_kategori,
        CASE WHEN nama_kategori IN (SELECT KAP.nama_kategori FROM KATEGORI_APPAREL KAP, APPAREL AP WHERE KAP.nama_kategori = AP.kategori_apparel)
        THEN FALSE
        ELSE TRUE
        END AS DELETEABLE
        FROM KATEGORI_APPAREL;
        """)
        response = {
            'result' : res,
            'role': request.session['role']
        }
        print(res)    
        return render(request, 'list_kategori_apparel.html', response)
    else:
        return HttpResponseRedirect('/login')


def delete_kategori_apparel(request, nama_kat_apparel):
    namaKategoriApparel = '' + nama_kat_apparel
    print(namaKategoriApparel)
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            make_query(
                f"DELETE FROM KATEGORI_APPAREL WHERE nama_kategori='{namaKategoriApparel}'"
            )
            return HttpResponseRedirect('/kategori_apparel/list/')
    else:
        return HttpResponseRedirect('/login')

def create_new_kategori_apparel(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                newApparelCategory = request.POST.get("newApparelCategory")
                make_query(
                    f"INSERT INTO KATEGORI_APPAREL VALUES ('{newApparelCategory}')"
                )
                return HttpResponseRedirect('/kategori_apparel/list/')
        return render(request, 'create_kategori_apparel.html')
    else:
        return HttpResponseRedirect('/login')