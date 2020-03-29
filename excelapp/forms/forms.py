from django import forms
from django.core.files.storage import default_storage

from excelapp.models import *
from excelapp.widgets import *
from users.models import *


class ChkForm(forms.Form):
     labels = ['チェック','複数チェック','ラジオボタン','動的選択肢１','動的選択肢２']
     CHOICE = [
          ('1','選択肢＜１＞'),
          ('2','選択肢＜２＞'),
          ('3','選択肢＜３＞')]

     SINGLE_CHOICE = [('1','OKなららチェック')]

     one = forms.MultipleChoiceField(
          label=labels[0],
          required=False,
          disabled=False,
          initial=[],
          choices=SINGLE_CHOICE,
          widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'})
               )     

     two = forms.MultipleChoiceField(
          label=labels[1],
          required=False,
          disabled=False,
          initial=[],
          choices=CHOICE,
          widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'})
              ) 

     four = forms.MultipleChoiceField(
          label=labels[3],
          required=False,
          disabled=False,
          widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'})
               )

     five = forms.MultipleChoiceField(
          label=labels[4],
          required=False,
          disabled=False,
          widget=forms.RadioSelect(attrs={'class': 'custom-control-input'})
               )

     department = forms.ModelMultipleChoiceField(
          label='部門',
          required=False,
          disabled=False,
          initial=[],
          queryset=Tm_Department.objects.all(),
          to_field_name='pk',
          # to_field_name='department_name',
          widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'})
               ) 

     service = forms.MultipleChoiceField(
          label='サービス',
          required=False,
          disabled=False,
          initial=[],
          choices=lambda: [(tm_Service.pk, tm_Service.service_name) for tm_Service in Tm_Service.objects.all()],
          widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'})
               ) 

class CustommCheckboxForm(forms.Form):
     service = forms.MultipleChoiceField(
          label='サービス',
          required=False,
          disabled=False,
          initial=[],
          choices=lambda: [(tm_Service.pk, tm_Service.service_name) for tm_Service in Tm_Service.objects.all()],
          widget=CustomCheckboxSelectMultiple()
               ) 
