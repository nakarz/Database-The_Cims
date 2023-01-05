from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from tools.tools import make_query

HOMEURL = "/home"
LOGINURL = "/login"


def index(request):
    return render(request, 'index.html')


def login(request, user, role):
    request.session['user'] = user
    request.session['role'] = role
    request.session['username'] = user["username"]

    return HttpResponseRedirect(HOMEURL)


def login_page(request):
    if 'user' in request.session:
        return HttpResponseRedirect(HOMEURL)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = "user"

        result = make_query(f"select * from pemain where username='{username}' and password='{password}'")
        if len(result) == 0:
            result = make_query(f"select * from admin where username='{username}' and password='{password}'")
            role = "admin"
            if len(result) == 0:
                return HttpResponseNotFound("User not found")

        user = user_result_to_map(result[0])
        return login(request, user, role)

    return render(request, 'login.html')


def home_page(request):
    if 'user' not in request.session:
        return HttpResponseRedirect(LOGINURL)

    model = {
        'role': request.session['role'],
        'username': request.session['username']
    }

    if request.session['role'] == 'user':
        user = make_query(f"select email, no_hp, koin from pemain "
                          f"where username='{request.session['username']}'")[0]
        model['email'] = user[0]
        model['phone'] = user[1]
        model['koin'] = user[2]

    return render(request, 'homepage.html', model)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")


def user_result_to_map(result):
    # regular user
    if len(result) == 5:
        result_map = {
            'username': result[0],
            'email': result[1],
            'password': result[2],
            'no_hp': result[3],
            'koin': result[4],
        }
        return result_map

    # admin
    result_map = {
        'username': result[0],
        'password': result[1],
    }
    return result_map


def register_player(request):
    if 'user' in request.session:
        return HttpResponseRedirect(HOMEURL)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        coin = 0

        username_exist = make_query(f"select * from akun where username='{username}'")
        if username_exist:
            return render(request, "register-player.html", {"error": "Username sudah digunakan"})

        # create player
        make_query(f"insert into pemain values "
                   f"('{username}', '{email}', '{password}', '{phone}', {coin})")

        user = {
            'username': username,
            'email': email,
            'password': password,
            'no_hp': phone,
            'koin': coin,
        }
        return login(request, user, "user")

    return render(request, "register-player.html")


def register_admin(request):
    if 'user' in request.session:
        return HttpResponseRedirect(HOMEURL)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        username_exist = make_query(f"select * from akun where username='{username}'")
        if username_exist:
            return render(request, "register-admin.html", {"error": "Username sudah digunakan"})

        # create admin
        make_query(f"insert into admin values "
                   f"('{username}', '{password}')")

        user = {
            'username': username,
            'password': password,
        }
        return login(request, user, "admin")

    return render(request, "register-admin.html")


def character_list(request):
    if 'user' not in request.session:
        return HttpResponseRedirect(LOGINURL)

    if request.session["role"] == "user":
        username = request.session["username"]
        characters = make_query(f"select * from tokoh where username_pengguna='{username}'")
    else:
        characters = make_query("select * from tokoh")

    return render(request, "character-list.html", {"characters": characters})


def character_detail(request):
    if 'user' not in request.session:
        return HttpResponseRedirect(LOGINURL)

    username = request.GET.get("username")
    char_name = request.GET.get("char_name")

    character = make_query(f"select * from tokoh where username_pengguna='{username}' and nama='{char_name}'")

    return render(request, "character-detail.html", {"character": character[0]})


def create_character(request):
    if 'user' not in request.session or request.session['role'] == 'admin':
        return HttpResponseRedirect(LOGINURL)

    if request.method == "POST":
        uname_user = request.session['username']
        nama_tokoh = request.POST.get('name')
        gender = request.POST.get('gender')
        skin = request.POST.get('skin')
        job = request.POST.get('job')

        make_query(
            f"""
            INSERT INTO TOKOH VALUES (
                '{uname_user}', 
                '{nama_tokoh}', 
                '{gender}', 
                'Aktif', 
                '0', 
                '100', 
                '0', 
                '0', 
                '{skin}', 
                '1', 
                'kreatif', 
                '{job}', 
                'RB001', 
                'MT001', 
                'RM001');
            """
        )

        return HttpResponseRedirect(HOMEURL)

    skin_colors = make_query("select * from warna_kulit")
    jobs = make_query("select nama from pekerjaan")

    return render(request, "create-character.html", {"skins": skin_colors, "jobs": jobs})


def update_character(request):
    if 'user' not in request.session:
        return HttpResponseRedirect(LOGINURL)

    username = request.session['username']
    char_name = request.GET.get('char_name')

    if request.method == "POST":
        hair = request.POST.get('hair')
        eyes = request.POST.get('eyes')
        house = request.POST.get('house')

        make_query(f"update tokoh "
                   f"set id_rambut='{hair}', id_mata='{eyes}', id_rumah='{house}'"
                   f"where username_pengguna='{username}' and nama='{char_name}'")

        return HttpResponseRedirect(HOMEURL)

    character = make_query(f"select * from tokoh where username_pengguna='{username}' and nama='{char_name}'")
    hairs = make_query(f"select id_koleksi from koleksi_tokoh "
                       f"where username_pengguna='{username}' and nama_tokoh='{char_name}'"
                       f"and id_koleksi in (select id_koleksi from rambut)")

    eyes = make_query(f"select id_koleksi from koleksi_tokoh "
                      f"where username_pengguna='{username}' and nama_tokoh='{char_name}'"
                      f"and id_koleksi in (select id_koleksi from mata)")

    houses = make_query(f"select id_koleksi from koleksi_tokoh "
                        f"where username_pengguna='{username}' and nama_tokoh='{char_name}'"
                        f"and id_koleksi in (select id_koleksi from rumah)")

    return render(request, 'update-character.html',
                  {'character': character[0], 'hairs': hairs, 'eyes': eyes, 'houses': houses})
