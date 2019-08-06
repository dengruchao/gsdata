from django.shortcuts import render, redirect

# Create your views here.
from django.http.response import JsonResponse, HttpResponse

# Create your views here.
from .forms import LoginForm
from wechat.forms import SearchForm
from .models import User
import traceback


def index(request):
    if not request.session.get('is_login', None):
        login_form = LoginForm()
        context = {
            'title': '小超数据登录-专业的媒体数据采集平台',
            'loginForm': login_form,
        }
        return render(request, 'login/login.html', context=context)
    form = SearchForm()
    user = User.objects.get(pk=request.session.get('user_id'))
    context = {
        'title': '小超数据-专业的媒体数据采集平台',
        'form': form,
        'user_info': {'username': user.username, 'times': user.times},
    }
    return render(request, 'login/index.html', context=context)


def login(request):
    if request.session.get('is_login', None):
        return redirect('/')
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username

                message = '登录成功'
                error_code = 0
            else:
                message = '密码错误'
                error_code = 1
        except:
            traceback.print_exc()
            message = '用户不存在'
            error_code = 2

        login_return = {
            'error_code': error_code,
            'msg': message,
        }
    return JsonResponse(login_return, safe=False)


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')


