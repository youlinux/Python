
from django.forms import ModelForm
from . import models
class CustomerModel(ModelForm):
    class Meta:
        model = models.Customer
        exclude=()

    def __init__(self,*args,**kwargs):
        super(CustomerModel,self).__init__(*args,**kwargs)
        # self.fields['qq'].widget.attrs["class"]="form-control" # bootstrap
        for fieldname in self.base_fields:
            field = self.base_fields[fieldname]
            print('前端',field)
            temp=field.widget.attrs=({'class':'form-control'})
            print('来自前端',temp)










