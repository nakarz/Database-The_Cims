from django.http import HttpResponseRedirect
from django.shortcuts import render
from tools.tools import make_query

LOGIN_URL = "/login"
MISSION_URL = "/main-mission"


def main_mission(request):
    if "user" not in request.session:
        return HttpResponseRedirect(LOGIN_URL)

    is_admin = request.session["role"] == "admin"
    if request.method == "GET":
        result = make_query(f"select * from misi_utama")

        deletable_mission = set()
        for data in result:
            mission_name = data.nama_misi
            referred = make_query(
                f"select * from menjalankan_misi_utama where nama_misi = '{mission_name}'"
            )

            if len(referred) == 0:
                deletable_mission.add(mission_name)

        return render(request, "main-mission.html",
                      {"missions": result, "deletable": deletable_mission, "is_admin": is_admin})


def mission_detail(request, mission_name):
    if "user" not in request.session:
        return HttpResponseRedirect(LOGIN_URL)

    mission = make_query(f"select * from misi where nama='{mission_name}'")

    time = mission[0].completion_time
    time_in_minutes = (time.hour * 60) + time.minute

    return render(request, "mission-detail.html", {"mission": mission[0],
                                                   "time": time_in_minutes})


def do_mission(request):
    if "user" not in request.session:
        return HttpResponseRedirect(LOGIN_URL)

    username = request.session["username"]
    is_admin = request.session["role"] == "admin"

    if is_admin:
        mission_list = make_query(f"select * from menjalankan_misi_utama")

    else:
        mission_list = make_query(f"select * from menjalankan_misi_utama "
                                  f"where username_pengguna='{username}'")

    return render(request, "do-mission.html", {"missions": mission_list, "is_admin": is_admin})


def create_main_mission(request):
    if "user" not in request.session or request.session["role"] != 'admin':
        return HttpResponseRedirect(LOGIN_URL)

    if request.method == "POST":
        name = request.POST.get("name")
        energy = request.POST.get("energy")
        social = request.POST.get("social")
        hunger = request.POST.get("hunger")
        req_energy = request.POST.get("req_energy")
        req_social = request.POST.get("req_social")
        req_hunger = request.POST.get("req_hunger")
        completion_time = request.POST.get("completion_time")
        coin = request.POST.get("coin")
        xp = request.POST.get("xp")
        desc = request.POST.get("desc")

        make_query(
            f"insert into misi values ("
            f" '{name}', {energy}, {social}, {hunger}, {req_energy}, {req_social}, {req_hunger}, "
            f" '{completion_time}', {coin}, {xp}, '{desc}'"
            f")"
        )
        make_query(f"insert into misi_utama values ('{name}')")

        return HttpResponseRedirect(MISSION_URL)

    return render(request, "create-main-mission.html")


def create_do_main_mission(request):
    if "user" not in request.session:
        return HttpResponseRedirect(LOGIN_URL)

    username = request.session["username"]

    characters = make_query(f"select nama from tokoh where username_pengguna='{username}'")
    missions = make_query(f"select nama_misi from misi_utama")

    if request.method == "POST":
        char_name = request.POST.get("char_name")
        main_mission_name = request.POST.get("main_mission_name")

        error = make_query(f"insert into menjalankan_misi_utama values "
                           f"('{username}', '{char_name}', '{main_mission_name}', 'Belum selesai')")

        if error:
            return render(request, "create-do-main-mission.html", {
                "characters": characters,
                "missions": missions,
                "error": error
            })
        return HttpResponseRedirect(MISSION_URL + "/do-mission")

    return render(request, "create-do-main-mission.html", {"characters": characters, "missions": missions})


def update_do_main_mission(request):
    if "user" not in request.session:
        return HttpResponseRedirect(LOGIN_URL)

    chara = request.GET.get("chara", "")
    mission_name = request.GET.get("mission_name", "")
    username = request.session["username"]
    mission = make_query(
        f"select * from menjalankan_misi_utama "
        f"where username_pengguna='{username}' and nama_misi='{mission_name}' and nama_tokoh='{chara}'"
    )

    if len(mission) == 0:
        return HttpResponseRedirect("/main-mission/do-mission")

    if request.method == "POST":
        status = request.POST.get("status").capitalize()

        if status != "Selesai" and status != "Belum selesai":
            return render(request, "update-do-main-mission.html", {
                "mission": mission[0],
                "error": "Status harus Selesai atau Belum selesai"
            })

        make_query(f"update menjalankan_misi_utama set status='{status}' "
                   f" where username_pengguna='{username}' and nama_misi='{mission_name}' and nama_tokoh='{chara}'")

        return HttpResponseRedirect(MISSION_URL + "/do-mission")

    return render(request, "update-do-main-mission.html", {"mission": mission[0]})


def delete_main_mission(request):
    if "user" not in request.session or request.session["role"] != 'admin':
        return HttpResponseRedirect(LOGIN_URL)

    if "name" in request.GET:
        mission_name = request.GET.get("name")
        make_query(f"delete from misi_utama where nama_misi='{mission_name}'")

    return HttpResponseRedirect(MISSION_URL)
