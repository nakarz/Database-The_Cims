from django.shortcuts import render
from tools.tools import make_query
from django.http.response import HttpResponseRedirect


def tampilan_job(request):
    if request.session.has_key('username'):
        res = make_query("""
        select *,
        case when nama in 
            (select p.nama from pekerjaan p, tokoh t, bekerja b, apparel a
            where p.nama = b.nama_pekerjaan and p.nama = t.pekerjaan and p.nama = a.nama_pekerjaan)
        then false
        else true
        end as deleteable
        from pekerjaan
        order by nama asc;""")
        
        response = {
            'result' : res,
            'role': request.session['role']
        }

        print(res)    
        return render(request, 'list_job.html', response)
    
    else:
        return HttpResponseRedirect('/login')



def create_job(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            return render(request, 'create_job.html')

        return HttpResponseRedirect('/job/list/')

    else:
        return HttpResponseRedirect('/login')  



def update_job(request, old_job):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            print("old_job = " + old_job)
            res = make_query(f"select * from pekerjaan where nama = '{old_job}';")
            
            print(res[0])
            return render(request, 'update_job.html', {'result' : res[0]})
        
        else:
            return HttpResponseRedirect('/job/list/')
   
    else:
        return HttpResponseRedirect('/login')



def delete_job(request, old_job):
    print("old_job = " + old_job)
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            make_query(f"delete from pekerjaan where nama = '{old_job}';")
        
        return HttpResponseRedirect('/job/list/')
   
    else:
        return HttpResponseRedirect('/login')



def update_base_honor(request, old_job):
    print("old_job = " + old_job)
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                new_honor = request.POST.get('new_honor')
                print(new_honor)
                make_query(f"update pekerjaan set base_honor = '{new_honor}' WHERE nama = '{old_job}';")
        
        return HttpResponseRedirect('/job/list/')
   
    else:
        return HttpResponseRedirect('/login')



def create_new_job(request):
    if request.session.has_key('username'):
        if request.session['role'] == 'admin':
            if request.method == 'POST':
                new_job = request.POST.get('new_job')
                new_base_honor = request.POST.get('new_base_honor')

                print(new_job)
                print(new_base_honor)
                make_query(f"insert into pekerjaan values ('{new_job}', '{new_base_honor}');")
            
        return HttpResponseRedirect('/job/list/')
    
    else:
        return HttpResponseRedirect('/login')