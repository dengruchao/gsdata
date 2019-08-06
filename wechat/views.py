from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse

# Create your views here.
from .forms import SearchForm
from login.models import User
import api

gsdata_api = api.GsDataAPI()


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params['posttime_start'] = params['posttime_start'].strftime('%Y-%m-%d')
            params['posttime_end'] = params['posttime_end'].strftime('%Y-%m-%d')
            params['sort'] = gsdata_api.sort_map[params['sort']]
            params['order'] = gsdata_api.order_map[params['order']]
            gsdata_api.get_msg_info(**params)
            user = User.objects.get(pk=request.session.get('user_id'))
            user.times -= (len(gsdata_api.news_list)//params.get('limit', 50) + 1)
            user.save()
            return JsonResponse({'times': user.times})


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


