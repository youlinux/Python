from django import forms
from app01 import models
class BookModelForm(forms.ModelForm):
    class Meta:
        model=models.Book
        #fields=('title','publication_date')
        exclude=()
        widgets = {
	    'title':forms.TextInput(attrs={'class':'form-control'}),	
	}
        
