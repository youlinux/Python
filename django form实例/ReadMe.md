
## 写一个较为详细的实例

## 以后可以在此基础上进行拓展和改进

关键代码如下

```python

# vim app01/forms.py

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django import forms
from django.core.exceptions import ValidationError


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class PublishForm(forms.Form):

    user_type_choice = (
        (0, u'普通用户'),
        (1, u'高级用户'),
    )

    user_type = forms.IntegerField(widget=forms.widgets.Select(choices=user_type_choice,
                                                                  attrs={'class': "form-control"}))

    title = forms.CharField(max_length=20,
                            min_length=5,
                            error_messages={'required': u'标题不能为空',
                                            'min_length': u'标题最少为5个字符',
                                            'max_length': u'标题最多为20个字符'},
                            widget=forms.TextInput(attrs={'class': "form-control",
                                                          'placeholder': u'标题5-20个字符'}))

    memo = forms.CharField(required=False,
                           max_length=256,
                           widget=forms.widgets.Textarea(attrs={'class': "form-control no-radius", 'placeholder': u'详细描述', 'rows': 3}))

    phone = forms.CharField(validators=[mobile_validate, ],
                            error_messages={'required': u'手机不能为空'},
                            widget=forms.TextInput(attrs={'class': "form-control",
                                                          'placeholder': u'手机号码'}))

    email = forms.EmailField(required=False,
                            error_messages={'required': u'邮箱不能为空','invalid': u'邮箱格式错误'},
                            widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': u'邮箱'}))

'''
def __init__(self, *args, **kwargs):
    super(SampleImportForm, self).__init__(*args, **kwargs)

    self.fields['idc'].widget.choices = models.IDC.objects.all().order_by('id').values_list('id','display')
    self.fields['business_unit'].widget.choices = models.BusinessUnit.objects.all().order_by('id').values_list('id','name')

Forms
'''

# vim app01/views.py

def test_form_view(request):
    if request.method == 'POST':
        request_form = PublishForm(request.POST)
        if request_form.is_valid():
            request_dict = request_form.clean()
            print(request_dict)
        return render(request,'test.html', {'pub_form':request_form})
    else:
        pub_form = PublishForm()
        return render(request,'test.html',{'pub_form':pub_form})


# vim templates/test.html

<div>
    <form method="post" action="">{% csrf_token %}

        <div>{{ pub_form.user_type }} {{ pub_form.errors.title }}</div>
        <div>{{ pub_form.title }}</div>
        <div>{{ pub_form.email }}</div>
        <div>{{ pub_form.phone }}</div>
        <div>{{ pub_form.memo }}</div>


        {% if pub_form.errors %}
            {{ pub_form.errors }}
        {% endif %}
        <input type="submit" value="提交">
    </form>

</div>

```

![](http://i.imgur.com/eW8zqlt.jpg)




