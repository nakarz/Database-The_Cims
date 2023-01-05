from django.http import HttpResponseRedirect
from django.shortcuts import render

from datetime import datetime
from tools.tools import make_query

LOGIN_URL = "/login"
FOODS_URL = "/foods"


def food_list(request):
    if 'user' not in request.session:
        return HttpResponseRedirect(LOGIN_URL)

    is_admin = request.session["role"] == "admin"
    foods = make_query("select * from makanan")

    deletable_food = set()
    for data in foods:
        food_name = data.nama
        referred = make_query(
            f"select * from makan where nama_makanan = '{food_name}'"
        )

        if len(referred) == 0:
            deletable_food.add(food_name)

    return render(request, "foods-list.html", {"foods": foods, "is_admin": is_admin, "deletable": deletable_food})


def eat_list(request):
    if 'user' not in request.session:
        return HttpResponseRedirect(LOGIN_URL)

    username = request.session["username"]
    is_admin = request.session["role"] == "admin"
    if is_admin:
        eats = make_query("select * from makan")
    else:
        eats = make_query(f"select * from makan where username_pengguna='{username}'")

    return render(request, "eats-list.html", {"eats": eats, "is_admin": is_admin})


def create_food(request):
    if 'user' not in request.session or request.session["role"] != 'admin':
        return HttpResponseRedirect(LOGIN_URL)

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        energy = request.POST.get('energy')
        hunger = request.POST.get('hunger')

        make_query(f"insert into makanan values ('{name}', {price}, {energy}, {hunger})")
        return HttpResponseRedirect(FOODS_URL)

    return render(request, "create-food.html")


def update_food(request):
    if 'user' not in request.session or request.session["role"] != 'admin':
        return HttpResponseRedirect(LOGIN_URL)

    food_name = request.GET.get("name", "")

    if request.method == "POST":
        price = request.POST.get('price')
        energy = request.POST.get('energy')
        hunger = request.POST.get('hunger')

        make_query(f"update makanan set harga={price}, tingkat_energi={energy}, tingkat_kelaparan={hunger} "
                   f"where nama='{food_name}'")

        return HttpResponseRedirect(FOODS_URL)

    food = make_query(f"select * from makanan where nama='{food_name}'")

    return render(request, "update-food.html", {"food": food[0]})


def delete_food(request):
    if "user" not in request.session or request.session["role"] != "admin":
        return HttpResponseRedirect(LOGIN_URL)

    if "name" in request.GET:
        food_name = request.GET.get("name")
        make_query(f"delete from makanan where nama='{food_name}'")

    return HttpResponseRedirect(FOODS_URL)


def create_eat(request):
    if "user" not in request.session or request.session["role"] != "user":
        return HttpResponseRedirect(LOGIN_URL)

    username = request.session["username"]
    characters = make_query(f"select nama from tokoh where username_pengguna='{username}'")
    foods = make_query("select nama from makanan")

    if request.method == "POST":
        current_datetime = datetime.now()
        char_name = request.POST['char_name']
        food_name = request.POST['food_name']

        error = make_query(f"insert into makan "
                           f"values ('{username}', '{char_name}', '{current_datetime}', '{food_name}')")
        if error:
            error = str(error)
            error_msg = error.split("CONTEXT")[0]
            return render(request, "create-eat.html",
                          {"characters": characters, "foods": foods, "error": error_msg})

        return HttpResponseRedirect(FOODS_URL + "/eat")

    return render(request, "create-eat.html", {"characters": characters, "foods": foods})
