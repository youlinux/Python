

from django.shortcuts import render,HttpResponse
from forms import PublishForm
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
