import time

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from my_task import models
from my_user.views import is_login, get_userid, get_user, get_user_by_id


# 主页
def index(request):
    return render(request, 'index.html')

# 创建任务
# 导航页
@is_login
def nav(request):
    if request.method == "GET":
        return render(request, "nav.html")

# 创建任务
# 登录验证
@is_login
def create_task(request):
    if request.method == "POST":
        result = {'state': '0', 'info': '任务创建成功！'}
        title = request.POST.get('title', None)
        detail = request.POST.get('detail', None)
        price = request.POST.get('price', None)
        sex_preference = request.POST.get('sex_preference', None)
        deadline = request.POST.get('deadline', None)
        user_id = get_userid(request)
        if title and price:
            task_id = time.strftime('%Y%m%d', time.localtime(time.time())) + "00"
            while True:
                if len(models.TaskInfo.objects.filter(task_id=task_id)) == 0:
                    break
                task_id = str(int(task_id) + 1)
            print("新建任务：", task_id, title, detail, price, user_id, deadline, 0)
            try:
                user = get_user(request)

                if user.user_price > int(price):
                    models.TaskInfo.objects.create(task_id=task_id, task_title=title, task_detail=detail,
                                                   task_price=float(price), task_sex_preference=sex_preference,
                                                   user_id=user_id, deadline=deadline, task_status=0)
                    user.user_price -= int(price)
                    user.save()
                else:
                    result = {'state': '-9', 'info': '您的余额不足，请充值后再发布任务！'}
            except Exception:
                result = {'state': '-2', 'info': '服务器错误请稍后尝试！'}
        else:
            result = {'state': '-1', 'info': '任务标题不能为空！'}
        return JsonResponse(result, safe=False)
    else:
        return render(request, "add_task.html")


# 查找任务，当keyword为空时从查找所有任务
def query_tasks(request):
    keyword = request.GET.get('keyword', None)
    local_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    try:
        tasks = models.TaskInfo.objects.filter(deadline__gt=local_time, task_status=0)
        if keyword:
            tasks = tasks.filter(Q(task_title__contains=keyword) | Q(task_detail__contains=keyword))
    except Exception:
        result = [{'state': '-1', 'info': '服务器错误请稍后尝试！'}]
    else:
        if len(tasks) > 0:
            data = []
            for task in tasks:
                item = task.__dict__
                del item['_state']
                item['create_time'] = item['create_time'].strftime("%Y%m%d%H%M%S")
                item['deadline'] = item['deadline'].strftime("%Y-%m-%d %H:%M")
                data.append(item)
            print(data)
            data.sort(key=lambda x: x['create_time'], reverse=True)  # 按创建时间将任务列表降序排列，以保证新创建的任务在前
            result = [{'state': '0', 'info': '查询成功！'}, data]
        elif keyword:
            result = [{'state': '-2', 'info': '没有找到相关任务！'}]
        else:
            result = [{'state': '-3', 'info': '任务列表为空！'}]

    return JsonResponse(result, safe=False)


# 任务详情
@is_login
def task_info(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id', None)
        user_id = get_userid(request)
        try:
            task = models.TaskInfo.objects.get(task_id=task_id)
        except Exception:
            result = [{'state': '-1', 'info': '服务器错误请稍后尝试！'}]
        else:
            data = task.__dict__
            del data['_state']
            data['create_time'] = data['create_time'].strftime("%Y-%m-%d %H:%M")
            data['is_collected'] = len(models.TaskCollectInfo.objects.filter(user_id=user_id, task_id=task_id))
            # 任务领取状态码生成
            # 0表示可领取;
            # 1表示用户自己发布的任务他人已领取，可以确认结束；
            # 2表示该任务已完成；
            # -1表示用户自己发布的任务，还未被领取，不能被用户自己领取；
            # -2表示用户不符合任务性别要求，不能被用户领取；
            # -3表示该任务已被领取，不能被用户领取
            # -4表示该任务已被用户自己领取，不能被用户重复领取
            task_can_accept = '0'
            accept_info = models.TaskAcceptInfo.objects.filter(task_id=task_id)
            if task.task_status == 2:
                task_can_accept = '3'
                if models.TaskAcceptInfo.objects.get(task_id=task_id).user_id == user_id:
                    task_can_accept = '2'
            elif task.user_id == user_id:
                task_can_accept = '-1'
                if accept_info:
                    task_can_accept = '1'
            elif task.task_sex_preference != 0 and task.task_sex_preference != get_user(request).user_sex:
                task_can_accept = '-2'
            elif accept_info:
                task_can_accept = '-3'
                if models.TaskAcceptInfo.objects.get(task_id=task_id).user_id == user_id:
                    task_can_accept = '-4'

            data['task_can_accept'] = task_can_accept
            result = [{'state': '0', 'info': '查询成功！'}, data]
        return JsonResponse(result, safe=False)
    else:
        return render(request, "task_info.html")


# 领取任务
# 登录验证
@is_login
def accept_task(request):
    result = {}
    if request.method == "POST":
        task_id = request.POST.get('task_id', None)
        user_id = get_userid(request)
        try:
            task = models.TaskInfo.objects.get(task_id=task_id)
            # 用户领取验证，不是本人发起的任务、任务状态待领取、任务性别要求符合
            if task.user_id != user_id and task.task_status == 0 and (
                    task.task_sex_preference == 0 or task.task_sex_preference == get_user(request).user_sex):
                # 生成id
                accept_id = time.strftime('%Y%m%d', time.localtime(time.time())) + "00"
                while True:
                    if len(models.TaskAcceptInfo.objects.filter(accept_id=accept_id)) == 0:
                        break
                    accept_id = str(int(accept_id) + 1)
                # 领取任务
                if models.TaskAcceptInfo.objects.create(accept_id=accept_id, task_id=task_id, user_id=user_id):
                    task.task_status = 1  # 更改任务状态
                    task.save()  # 更新数据库
                    result = {'state': '0', 'info': '任务领取成功！'}

        except Exception as e:
            result = {'state': '-2', 'info': '服务器错误请稍后尝试！', 'error': e}
        return JsonResponse(result, safe=False)


# 确认任务完成
# 登录验证
@is_login
def enter_task(request):
    result = {}
    if request.method == "POST":
        task_id = request.POST.get('task_id', None)
        user_id = get_userid(request)
        try:
            initiate_user_evaluate = int(request.POST.get('evaluate', 3))
            task = models.TaskInfo.objects.get(task_id=task_id)
            accept_info = models.TaskAcceptInfo.objects.get(task_id=task_id)
            if task.user_id == user_id:
                # 更改任务领取信息
                accept_info.initiate_user_evaluate = initiate_user_evaluate
                accept_info.end_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                accept_info.save()
                # 更改任务状态信息
                task.task_status = 2
                task.save()
                # 将款项转给领取者
                user = get_user_by_id(accept_info.user_id)
                user.user_price += task.task_price
                user.save()
                result = {'state': '0', 'info': '任务确认成功！'}
        except Exception:
            result = {'state': '-2', 'info': '服务器错误请稍后尝试！'}
        return JsonResponse(result)


# 领取者评价任务
# 登录验证
@is_login
def evaluate_task(request):
    result = {}
    if request.method == "POST":
        task_id = request.POST.get('task_id', None)
        user_id = get_userid(request)
        try:
            accept_user_evaluate = int(request.POST.get('evaluate', 3))
            accept_info = models.TaskAcceptInfo.objects.get(task_id=task_id)
            if accept_info.user_id == user_id:
                # 更改任务领取信息
                accept_info.accept_user_evaluate = accept_user_evaluate
                accept_info.save()
                # 更改任务状态信息
                result = {'state': '0', 'info': '任务评价成功！'}
        except Exception:
            result = {'state': '-2', 'info': '服务器错误请稍后尝试！'}
        return JsonResponse(result)


# 获取用户发布的任务列表
@is_login
def get_my_task(request):
    if request.method == "POST":
        try:
            user_id = get_userid(request)
            my_tasks = models.TaskInfo.objects.filter(user_id=user_id)
            data = []
            for task in my_tasks:
                item = task.__dict__
                del item['_state']
                item['create_time_str'] = item['create_time'].strftime("%Y%m%d%H%M%S")
                item['create_time'] = item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                item['deadline'] = item['deadline'].strftime("%Y-%m-%d %H:%M")
                data.append(item)
            data.sort(key=lambda x: x['create_time_str'], reverse=True)  # 按创建时间将任务列表降序排列，以保证新创建的任务在前
            result = [{'state': '0', 'info': '查询成功！'}, data]
        except Exception:
            result = [{'state': '-2', 'info': '服务器错误请稍后尝试！'}]
        return JsonResponse(result, safe=False)


# 获取用户领取的任务列表
@is_login
def get_my_accept_task(request):
    if request.method == "POST":
        try:
            user_id = get_userid(request)
            my_accept_tasks = models.TaskAcceptInfo.objects.filter(user_id=user_id)
            data = []
            for accept_info in my_accept_tasks:
                item = models.TaskInfo.objects.get(task_id=accept_info.task_id).__dict__
                del item['_state']
                item['create_time'] = item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                item['deadline_str'] = item['deadline'].strftime("%Y%m%d%H%M")
                item['deadline'] = item['deadline'].strftime("%Y-%m-%d %H:%M")
                data.append(item)
            data.sort(key=lambda x: x['deadline_str'], reverse=True)  # 按创建时间将任务列表降序排列，以保证最近截止的任务在前
            result = [{'state': '0', 'info': '查询成功！'}, data]
        except Exception:
            result = [{'state': '-2', 'info': '服务器错误请稍后尝试！'}]
        return JsonResponse(result, safe=False)


# 获取一个用户的任务信息（发布任务数，领取任务数）
@is_login
def get_task_len(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get('user_id', None)
            if not user_id:
                user_id = get_userid(request)
            my_tasks = models.TaskInfo.objects.filter(user_id=user_id)
            my_accept_tasks = models.TaskAcceptInfo.objects.filter(user_id=user_id)
            data = {'task_length': len(my_tasks), 'accept_length': len(my_accept_tasks)}
            result = [{'state': '0', 'info': '查询成功！'}, data]
        except Exception:
            result = [{'state': '-2', 'info': '服务器错误请稍后尝试！'}]
        return JsonResponse(result, safe=False)


# 获取一个用户任务评价（平均）
@is_login
def get_evaluate(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get('user_id', None)
            if not user_id:
                user_id = get_userid(request)
            local_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
            tasks = models.TaskInfo.objects.filter(user_id=user_id, task_status=2)
            accept_task = models.TaskAcceptInfo.objects.filter(user_id=user_id, end_time__lt=local_time)
            evaluate = []
            for accept_info in accept_task:
                evaluate.append(accept_info.initiate_user_evaluate)
            for task in tasks:
                evaluate.append(models.TaskAcceptInfo.objects.get(task_id=task.task_id).accept_user_evaluate)
            print(evaluate)
            evaluate = list(filter(None, evaluate))
            evaluate_avg = 0
            if len(evaluate):
                evaluate_avg = sum(evaluate) / len(evaluate)
            data = {'evaluate_avg': "%.1f"%evaluate_avg}
            result = [{'state': '0', 'info': '查询成功！'}, data]
        except Exception:
            result = [{'state': '-2', 'info': '服务器错误请稍后尝试！'}]
        return JsonResponse(result, safe=False)

# 收藏或取消收藏任务
@is_login
def collect_task(request):
    if request.method == "POST":
        try:
            user_id = get_userid(request)
            task_id = request.POST.get('task_id', None)
            is_collected = bool(request.POST.get('is_collected', None) == '1')
            if is_collected:
                models.TaskCollectInfo.objects.get(user_id=user_id, task_id=task_id).delete()
                result = [{'state': '0', 'info': '取消收藏成功！'}]
            else:
                collect_id = time.strftime('%Y%m%d', time.localtime(time.time())) + "00"
                while True:
                    if len(models.TaskCollectInfo.objects.filter(collect_id=collect_id)) == 0:
                        break
                    collect_id = str(int(collect_id) + 1)
                models.TaskCollectInfo.objects.create(collect_id=collect_id, task_id=task_id, user_id=user_id)
                result = [{'state': '0', 'info': '收藏成功！'}]
        except Exception as e:
            result = [{'state': '-2', 'info': '服务器错误请稍后尝试！'}]
        return JsonResponse(result, safe=False)

# 获取用户收藏的任务
@is_login
def get_collect_tasks(request):
    try:
        user_id = get_userid(request)
        my_collect_tasks = models.TaskCollectInfo.objects.filter(user_id=user_id)
        data = []
        for my_collect_task in my_collect_tasks:
            item = models.TaskInfo.objects.get(task_id=my_collect_task.task_id).__dict__
            del item['_state']
            item['create_time'] = item['create_time'].strftime("%Y%m%d%H%M%S")
            item['deadline'] = item['deadline'].strftime("%Y-%m-%d %H:%M")
            data.append(item)
        result = [{'state': '0', 'info': '获取收藏任务列表成功！'}, data]
    except Exception:
        result = [{'state': '-2', 'info': '服务器错误请稍后尝试！'}]
    return JsonResponse(result, safe=False)
