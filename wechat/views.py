from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .forms import SearchForm
from login.models import User
import api
import pickle
import time

gsdata_api = api.GsDataAPI()
sort_by = '+posttime'


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        params = dict()
        params['wx_name'] = form.data.get('wx_name')
        params['limit'] = 50
        if form.data.get('posttime_range'):
            posttime_range = form.data.get('posttime_range').split(' - ')
            params['posttime_start'] = posttime_range[0].strip()
            params['posttime_end'] = posttime_range[1].strip()
        print(params)
        user = User.objects.get(pk=request.session.get('user_id'))
        if user.times <= 0:
            return HttpResponse('次数已用完')
        if request.session.get('user_name') == 'test':
            with open('test.pkl', 'rb') as f:
                gsdata_api.news_list = pickle.load(f)
            time.sleep(0.5)
        else:
            gsdata_api.get_msg_info(**params)
        # news_list_len = len(gsdata_api.news_list)
        # 防盗链
        # for i in range(news_list_len):
        #     gsdata_api.news_list[i]['news_img'] = 'http://img01.store.sogou.com/net/a/04/link?appid=100520029&url=' +\
        #                                           gsdata_api.news_list[i]['news_imgs'].split(';')[0]
        user.times -= (len(gsdata_api.news_list)//params.get('limit') + 1)
        user.save()
        return JsonResponse({'times': user.times})


def sort_result_internal(by):
    if by[0] == '-':
        reverse = False
    else:
        reverse = True
    if by[1:] == 'posttime':
        gsdata_api.news_list.sort(key=lambda x: x['news_%s'%by[1:]], reverse=reverse)
    else:
        gsdata_api.news_list.sort(key=lambda x: int(x['news_%s'%by[1:]]), reverse=reverse)


def sort_result(request):
    global sort_by
    by = request.GET.get('by', '+posttime')
    sort_result_internal(by)
    sort_by = by
    return JsonResponse({'success': True})


def result(request):
    page = request.GET.get('page', '1')
    if int(page) == 1:
        sort_result_internal(sort_by)
    news_num = len(gsdata_api.news_list)
    page_num = 10
    paginator = Paginator(gsdata_api.news_list, page_num)
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    # paginator data
    page = int(page)
    if news_num <= page_num:
        paginator_data = {'is_paginated': False}
    else:
        left = []
        right = []
        left_has_more = []
        right_has_more = []
        first = False
        last = False
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page == 1:
            right = page_range[page:page+2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        paginator_data = {
            'is_paginated': True,
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'num_pages': total_pages,
            'current_page': news_list.number,
        }

    context = {
        'newsList': news_list,
        'pg': paginator_data,
    }

    return render(request, 'wechat/result.html', context=context)


def download(request):
    filename = request.session.get('user_name') + '.xls'
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


