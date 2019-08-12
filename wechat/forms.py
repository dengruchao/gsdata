from django import forms


class SearchForm(forms.Form):
    wx_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    posttime_range = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'daterange form-control',
                'placeholder': '可空，表示所有历史文章',
            }
        )
    )

