from django import forms 

class  InputForm(forms.Form):
    
    status_id = forms.CharField(label='Twitt ID', max_length=100)

