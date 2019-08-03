from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

# Create your views here.
from .forms import SearchForm, LoginForm
import api

gsdata_api = api.GsDataAPI()


def login(request):
    print(request.POST)
    form = LoginForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
    return form.cleaned_data


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
        'login_form': login_form,
    }
    return render(request, 'wechat/index.html', context=context)
