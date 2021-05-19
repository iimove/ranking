from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rank.models import *
from django.contrib import auth
from django.http import JsonResponse


# Create your views here.

# 账号登录
@csrf_exempt
def login(request):
    if request.method == 'GET':
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        user = RankUser.objects.filter(username=username, password=password).first()

        if user:
            return redirect(reverse('rank:index'))

        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = RankUser.objects.filter(username=username, password=password).first()

        if user:
            session = request.session
            session['username'] = user.username
            session['password'] = user.password
            session.set_expiry(100)
            response = redirect(reverse('rank:index'))
            response.set_cookie('user', user, max_age=3000)

            return response
        else:

            return render(request, 'login.html', {'status': '账号密码不正确'})


# 验证登录状态
def check_login(func):
    def check(request, *args, **kwargs):
        username = request.session.get('username', None)
        if username:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('rank:login'))

    return check


# 登出
def logout(request):
    auth.logout(request)
    return redirect('/')


# 上传分数
@check_login
@csrf_exempt
def index(request):
    username = request.session.get('username')
    user = RankUser.objects.filter(username=username).first()
    if request.method == 'GET':
        return render(request, 'index.html', {'user': user})

    if request.method == 'POST':
        fraction = request.POST.get('fraction', None)
        if fraction:
            username = request.session.get('username', None)
            user = RankUser.objects.filter(username=username).first()

            if user:
                user.fraction = fraction
                user.save()
            else:
                RankUser.objects.create(userNumber=username, fraction=fraction)

            Rank.objects.all().delete()
            user_list = [user_obj for user_obj in RankUser.objects.all().order_by('-fraction')]
            n = 1
            for i in user_list:
                Rank.objects.create(user=i, rank=n)
                n = n + 1
                user.save()
            return render(request, 'index.html', {'user': user, 'status': '上传成功'})
        return render(request, 'index.html', {'user': user, 'status': '上传失败'})


# 查询排名
@check_login
@csrf_exempt
def rank(request):
    username = request.session.get('username')
    user = RankUser.objects.filter(username=username).first()
    if request.method == 'GET':
        return render(request, 'rank.html', {'user': user})
    if request.method == 'POST':
        try:
            start = int(request.POST.get('start'))
            end = int(request.POST.get('end'))
        except ValueError as e:
            return JsonResponse({'status': 'error'})
        user_list = [{'fraction': user_obj.fraction, 'userNumber': user_obj.userNumber, 'ranking': user_obj.rank.rank}
                     for user_obj in RankUser.objects.all().order_by('-fraction')[start - 1:end]]

        return render(request, 'rank.html', locals())
