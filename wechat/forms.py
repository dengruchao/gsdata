from django import forms


class SearchForm(forms.Form):
    wx_name = forms.CharField(max_length=100, required=True, label='微信号',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    posttime_start = forms.DateField(label='发布日期开始', required=False, widget=forms.DateInput(attrs={'class': 'datetime form-control'}))
    posttime_end = forms.DateField(label='发布日期结束', required=False, widget=forms.DateInput(attrs={'class': 'datetime form-control'}))
    keywords = forms.CharField(label='关键词', max_length=200, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    order = forms.ChoiceField(label='排序方式', choices=((1, '降序'), (2, '升序')), initial=1,
                              widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    sort = forms.ChoiceField(label='排序字段', choices=((1, '发布日期'), (2, '阅读数'), (3, '点赞数')), initial=1,
                             widget=forms.Select(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

