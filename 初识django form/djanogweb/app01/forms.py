from django import forms

class BookForm(forms.Form):
    title=forms.CharField(max_length=10)
    #publisher_id=forms.IntegerField(widget=forms.Select)
    publication_date=forms.DateField()


