from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .forms import SearchForm
import api

gsdata_api = api.GsDataAPI()


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
            news_list = gsdata_api.get_msg_info(**params)
        return HttpResponse(str(news_list))


def index(request):
    form = SearchForm()
    context = {
        'title': '微信公众号历史文章',
        'form': form,
    }
    return render(request, 'wechat/index.html', context=context)
