from django.shortcuts import render
from tools.tools import make_query
from django.http.response import HttpResponseRedirect
from datetime import *


def tampilkan_bekerja(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            res = make_query(
                """
                select username_pengguna, nama_tokoh, nama_pekerjaan, timestamp, jumlah_keberangkatan, honor
                from bekerja order by username_pengguna,nama_tokoh asc;""")

        else:
            uname_user = request.session['username']
            print(uname_user)
            res = make_query(
                f"""
                select nama_tokoh, nama_pekerjaan, timestamp, jumlah_keberangkatan, honor
                from bekerja
                where username_pengguna = '{uname_user}'
                order by nama_tokoh asc;""")

        response = {
            'result' : res,
            'role': request.session['role']
        }

        print(res)
        return render(request, 'list_bekerja.html', response)

    else:
        return HttpResponseRedirect('/login')



def start_work(request):
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            uname_user = request.session['username']
            res = make_query(
                f"""
                select t.nama, t.pekerjaan, p.base_honor
                from tokoh t, pekerjaan p
                where t.username_pengguna = '{uname_user}' and p.nama = t.pekerjaan
                """
            )

            print(res)    
            return render(request, 'mulai_bekerja.html', {'result' : res})

    else:
        return HttpResponseRedirect('/login')



def create_bekerja(request, nama_tokoh, pekerjaan, base_honor):
    print("nama_tokoh = " + nama_tokoh)
    print("nama pekerjaan = " + pekerjaan)
    print("base honor = " + base_honor)
    
    if request.session.has_key('username'):
        if request.session['role'] != 'admin':
            uname_user = request.session['username']
            print(uname_user)

            res = check(nama_tokoh, pekerjaan, uname_user)
            current_datetime = datetime.now()

            level = make_query(f"select distinct level from tokoh where nama = '{nama_tokoh}';")
            level_tokoh = level[0][0]
            salary = level_tokoh * base_honor

            if res:
                make_query(f"""
                update bekerja 
                set jumlah_keberangkatan = jumlah_keberangkatan + 1
                where nama_tokoh = '{nama_tokoh}' and nama_pekerjaan = '{pekerjaan}';""")
            
            else:
                make_query(f"insert into bekerja values ('{uname_user}', '{nama_tokoh}', '{current_datetime}', '{pekerjaan}', 1, '{salary}');")

        return HttpResponseRedirect('/bekerja/list/')
   
    else:
        return HttpResponseRedirect('/login')



def check(nama_tokoh, pekerjaan, uname_user):
    res = make_query(f"select nama_tokoh from bekerja where username_pengguna = '{uname_user}';")
    tokoh = []

    for x in res:
        nama = x[0]
        tokoh.append(nama)


    for i in tokoh:
        if nama_tokoh == i:
            if (checkpekerjaan(nama_tokoh, pekerjaan)):
                return True

    return False

def checkpekerjaan(nama_tokoh, pekerjaan):
    res = make_query(f"select nama_pekerjaan from bekerja where nama_tokoh = '{nama_tokoh}';")
    list_pekerjaan = []

    for x in res:
        kerjaan = x[0]
        list_pekerjaan.append(kerjaan)

    for i in (list_pekerjaan):
        if (pekerjaan) == i:
            return True

    return False
