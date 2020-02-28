import time
import random

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from base import MD5
from my_user import models

PSD_STR = "ch2019"  # 用于密码加密的字符串


# 登录状态返回（返回isLogin）
def login_status(request):
    if 'username' in request.session:
        return JsonResponse({'isLogin': 'true'})
    else:
        return JsonResponse({'isLogin': 'false'})


# 登陆验证（函数修饰器）
def is_login(fn):
    def inner(request, *args, **kwargs):
        if 'username' in request.session:
            return fn(request, *args, **kwargs)
        else:
            # 如果用户未登录
            if request.method == "GET":
                # 301重定向到登录界面
                return HttpResponseRedirect('/user/login')
            else:
                return {'state': '-11', 'info': '请登录！'}

    return inner


# 获取用户对象
def get_user(request):
    return models.UserInfo.objects.get(user_id=get_userid(request))


# 获取用户对象
def get_user_by_id(user_id):
    return models.UserInfo.objects.get(user_id=user_id)


# 获取用户名（返回request的用户名）
def get_username(request):
    if 'username' in request.session:
        return request.session['username']


# 获取用户编号（返回request来自的用户编号）
def get_userid(request):
    if 'userid' in request.session:
        return request.session['userid']


def index(request):
    return render(request, "user/index.html")


# 登陆
def login(request):
    if request.method == "POST":
        identity_code = request.POST['identity_code']
        username = request.POST['username']
        password = request.POST['password']

        keep_login = bool(request.POST.get('keep_login', None))
        result = {}
        if identity_code.upper() == request.session['img_identify_code'].upper():
            result = {'state': '-2', 'info': '用户名或密码错误！'}
            if models.UserInfo.objects.filter(user_name=username):
                print("test")
                user_obj = models.UserInfo.objects.get(user_name=username)
                if user_obj.user_password == MD5.get_str_md5(password + PSD_STR):
                    print(username, "Login successful.", keep_login)
                    request.session['username'] = username
                    request.session['password'] = password
                    request.session['userid'] = user_obj.user_id
                    request.session.set_expiry(0)
                    if keep_login:
                        request.session.set_expiry(7 * 24 * 60 * 60)
                    result = {'state': '0', 'info': '登陆成功！'}
        else:
            result = {'state': '-1', 'info': '验证码错误！'}
        return JsonResponse(result, safe=False)
    else:
        if 'username' in request.session and 'password' in request.session:
            username = request.session['username']
            password = request.session['password']
            if models.UserInfo.objects.get(user_name=username).user_password == MD5.get_str_md5(password + PSD_STR):
                return HttpResponseRedirect('/')
        return render(request, 'user/login.html')


# 注销
def logout(request):
    if request.method == "GET":
        if 'username' in request.session and 'password' in request.session:
            del request.session['username']
            del request.session['password']
            del request.session['userid']
        return HttpResponseRedirect('/user/login')


# 注册
def register(request):
    if request.method == "POST":
        identify_code = request.POST['identify_code']
        username = request.POST['username']
        password = MD5.get_str_md5(request.POST['password'] + PSD_STR)
        sex = request.POST['sex']
        email = request.POST['email']
        result = {}
        if identify_code == request.session['phone_identify_code']:
            if models.UserInfo.objects.filter(user_name=username):
                result = {'state': '-2', 'info': '该用户名已被使用，请更换用户名后尝试！'}
            else:
                tel = request.session['tel']
                id = time.strftime('%Y%m%d', time.localtime(time.time())) + "00"
                while True:
                    if len(models.UserInfo.objects.filter(user_id=id)) == 0:
                        break
                    id = str(int(id) + 1)
                if models.UserInfo.objects.create(user_id=id, user_name=username, user_password=password, user_tel=tel,
                                                  user_sex=sex, user_email=email):
                    result = {'state': '0', 'info': '注册成功！'}
                else:
                    result = {'state': '-3', 'info': '服务器错误请稍后尝试！'}
        else:
            result = {'state': '-1', 'info': '验证码输入错误！'}

        return JsonResponse(result, safe=False)

    else:
        return render(request, 'user/register.html')


# 更改密码（通过密码，需要登陆）
@is_login
def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        new_password = request.POST['new_password']
        result = {}
        user_obj = models.UserInfo.objects.get(user_id=get_userid(request))
        if user_obj.user_password == MD5.get_str_md5(password + PSD_STR):
            user_obj.user_password = MD5.get_str_md5(new_password + PSD_STR)
            user_obj.save()
            result = {'state': '0', 'info': '密码更改成功！'}
        else:
            result = {'state': '-1', 'info': '旧密码输入错误！'}
        return JsonResponse(result, safe=True)

    else:
        return render(request, "user/rePassword.html")


# 更改密码（通过密码，需要登陆）
@is_login
def set_info(request):
    if request.method == "POST":
        result = {}
        try:
            username = request.POST['username']
            tel = request.POST['tel']
            email = request.POST['email']
            result = {}
            user_obj = models.UserInfo.objects.get(user_id=get_userid(request))
            user_obj.user_name = username
            user_obj.user_tel = tel
            user_obj.user_email = email
            user_obj.save()
            result = {'state': '0', 'info': '用户信息更改成功！'}
        except Exception as e:
            result = {'state': '-9', 'info': '用户信息更改失败，您新设置的用户名可能已被其他用户使用，请更改后重试！'}
        finally:
            return JsonResponse(result, safe=True)


# 通过手机号码更改密码（忘记密码）
def reset_password_by_phone(request):
    if request.method == "POST":
        identify_code = request.POST['identify_code']
        password = MD5.get_str_md5(request.POST['password'] + PSD_STR)
        result = {}
        if identify_code == request.session['phone_identify_code']:
            obj = models.UserInfo.objects.get(user_tel=request.session['tel'])
            obj.user_password = password
            obj.save()
            result = {'state': '0', 'info': '密码更改成功！'}
        else:
            result = {'state': '-1', 'info': '验证码输入错误！'}
        return JsonResponse(result, safe=False)
    else:
        return render(request, "user/rePasswordPhone.html")


# 图片验证码及手机短信验证码（GET请求返回验证码图片，POST请求发送验证码短信）
def identify_code(request):
    if request.method == "POST":
        # post请求发送手机验证码
        tel = request.POST.get('tel', None)
        result = {}
        if models.UserInfo.objects.filter(user_tel=tel) and request.POST.get("type", None):
            result = {'state': '-1', 'info': '该手机号码已注册，请更改手机号码后尝试！'}
        else:
            code = str(random.randint(10000, 99999))
            if dx_identify_code(tel, code):
                # 将手机号码及随机生成的5位验证码放入session
                # 用于后面验证
                # 5分钟有效
                request.session['tel'] = tel
                request.session['phone_identify_code'] = code
                request.session.set_expiry(5 * 60)
                # codeStr = "【校园帮】验证码：" + code + "。该验证码五分钟有效，请尽快输入。此验证码仅供身份验证使用，请勿泄露给他人使用。"
                # print(codeStr)
                result = {'state': '0', 'info': '验证码发送成功，请注意手机查收！'}
            else:
                result = {'state': '-2', 'info': '验证码发送失败，请联系管理员！'}
        return JsonResponse(result, safe=False)
    else:
        # get请求发送图片验证码

        # 引入绘图模块
        from PIL import Image, ImageDraw, ImageFont
        # 定义变量，用于画面的背景色、宽、高
        bg_color = (random.randrange(20, 100), random.randrange(
            20, 100), random.randrange(20, 100))
        width = 140
        height = 50
        # 创建画面对象
        im = Image.new('RGB', (width, height), bg_color)
        # 创建画笔对象
        draw = ImageDraw.Draw(im)
        # 调用画笔的point()函数绘制噪点
        for i in range(0, 100):
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)
        # 随机生成5位验证码
        code = ''.join(
            [random.choice('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM') for i in range(5)])
        print(code)
        # 构造字体对象
        font1 = ImageFont.truetype(r'./my_user/font/font1.otf', 40)
        font2 = ImageFont.truetype(r'./my_user/font/font2.otf', 40)
        # 构造字体颜色
        fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
        fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
        fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
        fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
        # 绘制5个字符
        draw.text((10, 10), code[0], font=font1, fill=fontcolor1)
        draw.text((30, 5), code[1], font=font2, fill=fontcolor2)
        draw.text((60, 10), code[2], font=font1, fill=fontcolor3)
        draw.text((80, 5), code[3], font=font2, fill=fontcolor4)
        draw.text((110, 10), code[4], font=font1, fill=fontcolor4)
        # 释放画笔
        del draw

        import io
        buf = io.BytesIO()
        # 将图片保存在内存中，文件类型为png
        im.save(buf, 'png')
        # 将内存中的图片数据返回给客户端，MIME类型为图片png
        response = HttpResponse(buf.getvalue(), 'image/png')

        # 存入session，用于做进一步验证
        request.session['img_identify_code'] = code
        request.session.set_expiry(5 * 60)

        return response


def dx_identify_code(tel, code):
    # 短信应用SDK AppID
    appid = 1400201395  # SDK AppID是1400开头

    # 短信应用SDK AppKey
    appkey = "b01087f69fcb040685b93b0448a20ad0"

    # 需要发送短信的手机号码
    phone_numbers = [str(tel)]

    # 短信模板ID，需要在短信应用中申请
    template_id = 311413  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
    # templateId 7839 对应的内容是"您的验证码是: {1}"
    # 签名
    sms_sign = "东聿隹"

    from qcloudsms_py import SmsSingleSender
    from qcloudsms_py.httpclient import HTTPError

    ssender = SmsSingleSender(appid, appkey)
    params = [code]  # 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
    result = {}
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
                                         template_id, params, sign=sms_sign, extend="",
                                         ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    bool_result = False
    if result['result'] == 0:
        bool_result = True

    return bool_result


# 用户主页
@is_login
def user_info(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id', None)
        if not user_id:
            user_id = get_userid(request)
        try:
            user = models.UserInfo.objects.get(user_id=user_id)
        except Exception:
            result = [{'state': '-1', 'info': '服务器错误请稍后尝试！'}]
        else:
            data = user.__dict__
            del data['_state']
            del data['user_register_time']
            result = [{'state': '0', 'info': '查询成功！'}, data]
        return JsonResponse(result, safe=False)
    else:
        return render(request, "user/index.html")


# 充值
@is_login
def add_price(request):
    result = {}
    if request.method == "POST":
        try:
            price = int(request.POST.get('price', 0))
            user = get_user(request)
            user.user_price += price
            user.save()
            result = {'state': '0', 'info': '充值成功！'}
        except Exception:
            result = {'state': '-2', 'info': '服务器错误请稍后尝试！'}
        return JsonResponse(result)


# 用户协议
def user_protocol(request):
    return render(request, 'user/user_protocol.html')