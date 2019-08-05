from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.http.response import JsonResponse

# Create your views here.
from .forms import SearchForm, LoginForm
from .models import User
import api

gsdata_api = api.GsDataAPI()


def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        error_code = -1
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                message = '登录成功'
                error_code = 0
            else:
                message = '密码错误'
                error_code = 1
        except:
            message = '用户不存在'
            error_code = 2

        login_return = {
            'error_code': error_code,
            'msg': message
        }
    return JsonResponse(login_return, safe=False)


def msg_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params['posttime_start'] = params['posttime_start'].strftime('%Y-%m-%d')
            params['posttime_end'] = params['posttime_end'].strftime('%Y-%m-%d')
            params['sort'] = gsdata_api.sort_map[params['sort']]
            params['order'] = gsdata_api.order_map[params['order']]
            print(params)
            gsdata_api.get_msg_info(**params)
            return render(request, 'wechat/result.html', context={'title': '查询结果-%s'%params['wx_name']})


def export_excel(request):
    filename = 'test.xls'
    gsdata_api.save_as_excel(filename)

    def file_iterator(file_name):
        with open(file_name, 'rb')as f:
            while True:
                c = f.read(512)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename=%s" % filename
    return response


def index(request):
    form = SearchForm()
    login_form = LoginForm()
    context = {
        'title': '微信公众号历史文章',
        'form': form,
        'loginForm': login_form,
    }
    return render(request, 'wechat/index.html', context=context)
