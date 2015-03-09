# -*- coding: utf-8 -*-

from django import forms 

class  InputForm(forms.Form):
    
    twit_id = forms.CharField(label='Twitt ID', max_length=100)

