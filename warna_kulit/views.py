from django.shortcuts import render
from django.db import connection
from tools.tools import make_query
from django.http.response import HttpResponseRedirect, JsonResponse

LOGIN_URL = '/login'
WARNA_KULIT_LIST = '/warna_kulit/list/'

def fetch_all_warna_kulit(request):
    if request.session.has_key('username'):
        res = make_query("""
            select kode, 
            case when kode in (select wk.kode from warna_kulit wk, tokoh t where wk.kode = t.warna_kulit) 
            then false
            else true
            end as deleteable
            from warna_kulit;
            """
        )

        response = {
            'result' : res,
            'role': request.session['role']
        }

        print(res)
           
        return render(request, 'list_warna_kulit.html', response)


    else:
        return HttpResponseRedirect(LOGIN_URL)

def delete_warna_kulit(request, wk_kode):
    real_wk_kode = '#' + wk_kode
    print("real_wk_kode = " + real_wk_kode)
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            make_query(f"DELETE FROM warna_kulit WHERE kode = '{real_wk_kode}';")
           
        return HttpResponseRedirect(WARNA_KULIT_LIST)

    else:
        return HttpResponseRedirect(LOGIN_URL)

def create_page(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'create_warna_kulit.html')
            
        return HttpResponseRedirect(WARNA_KULIT_LIST)
        
    else:
        return HttpResponseRedirect(LOGIN_URL)

def create_new_warna_kulit(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                new_code = request.POST['new_code']
                print("new_code is " + new_code)
                result = checkValidityNewCode(new_code)
                print(result)
                # CEK DULU DATANYA UDH ADA ATAU BELUM BIAR GA ERROR (kalau mau handle 😁)
                if result:
                    print("MASUK IF RESULT")
                    make_query(f"INSERT INTO WARNA_KULIT (kode) VALUES ('{new_code}');")
                    response = {
                        "id": 1,
                        "content": "Kode warna berhasil ditambahkan!"
                    }

                    return JsonResponse(response)

                else :
                    response = {
                        "id": 2,
                        "title" : "Kode warna tidak valid!",
                        "content": "Kode warna harus terdiri dari 7 karakter hexadecimal yang diawali dengan '#'",
                        "closing": "Silahkan masukkan ulang kode warna!"
                    }

                    return JsonResponse(response)

        return HttpResponseRedirect(WARNA_KULIT_LIST)
        
    else:
        return HttpResponseRedirect(LOGIN_URL)

def checkValidityNewCode(new_code):
    hexa = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','A','B','C','D','E','F']

    if len(new_code) < 7 or new_code[0] != '#':
        return False

    for i in range(1, len(new_code)):
        if new_code[i] not in hexa:
            return False
    
    return True