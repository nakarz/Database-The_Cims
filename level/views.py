from django.shortcuts import render
from django.db import connection
from tools.tools import make_query
from django.http.response import HttpResponseRedirect

LOGIN_URL = '/login'
LEVEL_LIST = '/level/list/'

def fetch_all_level(request):
    if request.session.has_key('username'):
        res = make_query("""
            select *, 
            case when level in (select l.level from level l, tokoh t where l.level = t.level) 
            then false
            else true
            end as deleteable
            from level
            order by level asc;
            """
        )

        response = {
            'result' : res,
            'role': request.session['role']
        }
        
        print(res)
           
        return render(request, 'list_level.html', response)


    else:
        return HttpResponseRedirect(LOGIN_URL)

def delete_level(request, old_level):
    print("old_level = " + old_level)
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            make_query(f"DELETE FROM level WHERE level = '{old_level}';")
            
        return HttpResponseRedirect(LEVEL_LIST)

    else:
        return HttpResponseRedirect(LOGIN_URL)

def update_page(request, old_level):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            print("old_level = " + old_level)
            res = make_query(f"select * from level where level = {old_level};")
            print(res[0])

            return render(request, 'update_level.html', {'result' : res[0]})
        
        else:
            return HttpResponseRedirect(LEVEL_LIST)
    
    else:
        return HttpResponseRedirect(LOGIN_URL)

def update_xp(request, old_level):
    print("old_level = " + old_level)
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                new_xp = request.POST.get('new_xp')
                print(new_xp)
                make_query(f"UPDATE level set xp = '{new_xp}' WHERE level = '{old_level}';")
                
        return HttpResponseRedirect(LEVEL_LIST)

    else:
        return HttpResponseRedirect(LOGIN_URL)

def create_page(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'create_level.html')

        return HttpResponseRedirect(LEVEL_LIST)
    else:
        return HttpResponseRedirect(LOGIN_URL)  

def create_new_level(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                new_level = request.POST.get('new_level')
                new_xp = request.POST.get('new_xp')

                print(new_level)
                print(new_xp)
                # CEK DULU DATANYA UDH ADA ATAU BELUM BIAR GA ERROR (kalau mau handle 😁)
                make_query(f"INSERT INTO LEVEL VALUES ('{new_level}', '{new_xp}');")
                
        return HttpResponseRedirect(LEVEL_LIST)

    else:
        return HttpResponseRedirect(LOGIN_URL)
