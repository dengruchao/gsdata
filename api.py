import hashlib
import base64
import requests
import pickle
import xlwt
import os


class GsDataAPI:
    def __init__(self):
        self.app_key = 'b523947e120c8ee8a88cb278527ddb5a'
        self.app_secret = '1962972fee15606cd1ad1dc8080bb289'
        self.sort_map = {'1': 'posttime', '2': 'readnum', '3': 'likenum'}
        self.order_map = {'1': 'desc', '2': 'asc'}

        self.news_list = []

    def _gen_access_token(self, params, router):
        params_list = sorted(params.items(), key=lambda x: x[0])
        params_str = ''.join([''.join(params) for params in params_list])
        params_final = '%s_%s_%s' % (self.app_secret, params_str, self.app_secret)
        m = hashlib.md5()
        m.update(params_final.encode('utf-8'))
        sign = m.hexdigest()
        C = base64.b64encode(bytes(self.app_key+':'+sign+':'+router, encoding='utf-8'))
        return C

    def get_msg_info(self, **kwargs):
        '''
        参数	        类型	可空	默认	    描述	        示例
        wx_name	        String  YES	    ---	        微信号	        rmrbwx
        posttime_start	String	YES	    ---	        文章发布开始时间	2018-08-20 10:00:00
        posttime_end	String	YES	    ---	        文章发布结束时间	2018-09-07 06:00:00（不含）
        entertime_start	String	YES	    ---	        文章入库开始时间	2018-08-08 12:00:00
        entertime_end	String	YES	    ---	        文章入库结束时间	2018-08-20 22:00:00（不含）
        keywords	    String	YES	    ---	        检索词	        aaa+bbb,ccc,ddd+eee
        order	        String	YES	    desc	    排序方式	    desc
        sort	        String	YES	    posttime	排序字段	    posttime
        page	        Integer	YES	    1	        第几页	        1
        limit	        Integer	YES	    50	        每页显示条数	    20
        sn	            String	YES	    --	        sn	            aabbcc
        '''
        kwargs['limit'] = str(kwargs.get('limit', 50))
        if kwargs.get('posttime_start') is not None:
            kwargs['posttime_start'] += ' 00:00:00'
        if kwargs.get('posttime_end') is not None:
            kwargs['posttime_end'] += ' 24:00:00'

        sort_type = kwargs.get('sort')
        if sort_type in [None, 'posttime']:
            router = '/weixin/article/search1'
        elif sort_type == 'readnum':
            router = '/weixin/article/search2'
        elif sort_type == 'likenum':
            router = '/weixin/article/search3'
        else:
            return None

        params = kwargs
        self.news_list = []
        while True:
            url = 'http://databus.gsdata.cn:8888/api/service'
            C = self._gen_access_token(params, router)
            r = requests.get(url, headers={'access-token': C}, params=params)
            r_js = r.json()
            if not r_js['success']:
                print(r_js)
            data = r_js['data']
            num_found = data['numFound']
            pagination = data['pagination']
            page = pagination['page']
            if page == 1:
                print('总计%d篇文章' % num_found)
            self.news_list.extend(data['newsList'])
            news_list_len = len(self.news_list)
            print('已获取%d篇' % (news_list_len))
            if news_list_len >= num_found:
                break
            params['page'] = str(page + 1)

        # with open('test.pkl', 'wb') as f:
        #     pickle.dump(self.news_list, f)

    def save_as_excel(self, filename):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet0')
        header = ['标题', '摘要', '发布时间', '作者', '阅读数', '点赞数', '链接']
        for i, field in enumerate(header):
            ws.write(0, i, field)
        col_width = [10000, 10000, 5000, 5000, 5000, 5000, 20000]
        col_count = len(col_width)
        for i in range(col_count):
            ws.col(i).width = col_width[i]

        row = 1
        for news in self.news_list:
            ws.write(row, 0, news['news_title'])
            ws.write(row, 1, news['news_digest'])
            ws.write(row, 2, news['news_posttime'])
            ws.write(row, 3, news['news_author'])
            ws.write(row, 4, news['news_read_count'])
            ws.write(row, 5, news['news_like_count'])
            ws.write(row, 6, news['news_url'])
            row += 1

        wb.save(filename)


class IDataApi:
    def __init__(self):
        self.api_key = 'vYpznyAwychvW7ur6HMbUx08YgO81ZX2eFpLytUGRTHeitTSUIONsZLpps3O18aY'
        self.data_json = None

    def get_msg_info(self, **kwargs):
        url = "http://api01.idataapi.cn:8000/post/weixin?apikey=%s" % self.api_key
        params = kwargs
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "close"
        }

        if not os.path.exists('idata.pkl'):
            r = requests.get(url, headers=headers, params=params)
            self.data_json = r.json()
            if self.data_json['retcode'] == '000000':
                with open('idata.pkl', 'wb') as f:
                    pickle.dump(r.json(), f)
            else:
                print(self.data_json['message'])
                return
        else:
            with open('idata.pkl', 'rb') as f:
                self.data_json = pickle.load(f)

        data_list = self.data_json['data']
        has_next = self.data_json['hasNext']
        page_token = self.data_json['pageToken']
        print(has_next)
        print(page_token)
        for data in data_list:
            print(data['title'])
            print(data['url'])
            print('')


if __name__ == '__main__':
    # api = GsDataAPI()
    # news_list = api.get_msg_info(wx_name='chaping321', posttime_start='2019-07-15', posttime_end='2019-07-28')

    idata_api = IDataApi()
    idata_api.get_msg_info(uid='chaping321', searchMode='top', beginDate='2018-03-01', endDate='2019-08-14')
