from django.shortcuts import render, HttpResponse, redirect
from app01 import models
import datetime
import json

#   滑动验证码
from app01.geetest import GeetestLib

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"


def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 滑动验证码登录
def pcajax_validate(request):
    if request.method == "POST":
        login_response = {"is_login": False, "error_msg": None}
        #  验证验证码
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        # 扩充 验证用户名密码
        if result:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = models.UserInfo.objects.filter(name=username, pwd=password).first()
            if user:
                login_response["is_login"] = True
                request.session['user'] = {"id": user.id, "name": username}

            else:
                login_response["error_msg"] = "username or password error"

        else:
            login_response["error_msg"] = "验证码错误"

        return HttpResponse(json.dumps(login_response))

    return HttpResponse("error")


# Create your views here.
def index(request):
    muds_dic = {}
    muds_l = []
    time_choices=models.Room_userinfo_date.time_choice
    if request.method == 'POST':
        date = request.POST.get("date")
        if date:
            muds = models.Room_userinfo_date.objects.filter(date=date).values('id', "room__name",
                                                                                                 "time",
                                                                                                 "UserInfo__name")
            print(muds)
        else:
            muds = models.Room_userinfo_date.objects.filter(date=datetime.datetime.now()).values('id', "room__name",
                                                                                                 "time",
                                                                                                 "UserInfo__name")
        # for mud in muds:
        #      muds_dic[mud["id"]]=mud
        # return  HttpResponse(json.dumps(muds_dic))
        for mud in muds:
            muds_l.append(mud)
        return HttpResponse(json.dumps(muds_l))
    rooms = models.Room.objects.all()

    # ym=date[:10]

    # muds=models.Room_userinfo_date.objects.all().values_list("time","date","room")
    # models.Room_userinfo_date.objects.update(date=datetime.datetime.now()).values_list("room__name","time","date")
    muds = models.Room_userinfo_date.objects.filter(date=datetime.datetime.now()).values('id', "room__name", "time",
                                                                                         "date", "UserInfo__name")
    # muds_l=[]
    # for mud in muds:
    #     muds_l.append(mud)

    return render(request, 'index.html', {"rooms": rooms,"time_choices":time_choices})




def login(request):
    return render(request, 'login.html')


def canceleRoom(request, mud_id):
    models.Room_userinfo_date.objects.filter(id=mud_id).delete()
    return HttpResponse('ok')


def saveReserve(request):
    reserve_bytes = request.body
    reserve_str = reserve_bytes.decode("utf-8")
    reserve_dic = json.loads(reserve_str)
    reserve_list = reserve_dic.get("reserve_list")
    print(reserve_list)
    for reverse in reserve_list:
        time = reverse.get("time")
        date = reverse.get("date")
        user_id = request.session.get("user").get("id")
        roomname = reverse.get("roomname")
        room = models.Room.objects.filter(name=roomname).first()
        models.Room_userinfo_date.objects.create(date=date, time=time, room=room, UserInfo_id=user_id)

    return HttpResponse('ok')
