# 文件：　comment/forms.py
import mistune

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='你是啷个嘛～',
        max_length=10,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 8%'}
        )
    )
    # website = forms.CharField(
    #     label='网站',
    #     max_length=100,
    #     widget=forms.widgets.URLInput(
    #         attrs={'class': 'form-control', 'style': 'width: 25%'}
    #     )
    # )
    content = forms.CharField(
        label='或许你想点评点评～',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 8:
            raise forms.ValidationError('你这写的也太少了～')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'content']
