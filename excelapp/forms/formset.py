import os
import shutil
from datetime import datetime

from django import forms
from django.core.files.storage import default_storage

from excelapp.models import Tm_Department, Tm_Service
from excelapp.utils.file_util import CustomFile
from excelapp.utils.form_utils import FormUtil

from django.forms import ModelChoiceField

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.department

class ServiceForm(forms.Form):
    delete_check = forms.BooleanField(
        label='削除',
        required=False,
        widget=forms.CheckboxInput(),
    )

    pk = forms.IntegerField(required=False)

    department_name = forms.CharField(
        label=Tm_Department._meta.get_field('department_name').verbose_name,
        max_length=Tm_Department._meta.get_field('department_name').max_length,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=False)

    service_name = forms.CharField(
        label=Tm_Service._meta.get_field('service_name').verbose_name,
        max_length=Tm_Service._meta.get_field('service_name').max_length,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=False)


    @property # propertyの時は　x.getterと同義
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        self._x = abs(v) # 更新前に何らかの処理をはさめる

    @x.deleter
    def x(self):
        self._x = None




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._x = None
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Tm_Service
        # fields = '__all__'
        fields = ('department', 'service_name', 'upload_file')
        # widgets = {
        #     'department': forms.TextInput(to_field_name='department_name'),
        #     'service_name': forms.TextInput(),
        # }






class ServiceCreateForm(forms.ModelForm):
    delete_check = forms.BooleanField(
        label='削除',
        required=False,
        widget=forms.CheckboxInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Tm_Service
        # fields = '__all__'
        fields = ('department', 'service_name', 'upload_file')
        # widgets = {
        #     'department': forms.TextInput(to_field_name='department_name'),
        #     'service_name': forms.TextInput(),
        # }

# これがモデルフォームセット
ServiceCreateFormSet = forms.modelformset_factory(
    Tm_Service, form=ServiceCreateForm, extra=0
)
