import os
import shutil
from datetime import datetime

from django import forms
from django.core.files.storage import default_storage

from excelapp.models import Tm_Department, Tm_Service
from excelapp.utils.file_util import CustomFile


class ServiceForm(forms.Form):
    department = forms.ModelChoiceField(
        label=Tm_Service._meta.get_field('department').verbose_name,
		queryset=Tm_Department.objects.all(),
		widget=forms.Select(attrs={'class':'form-control'}),
		empty_label='該当なし',
        required=True)
    service_name = forms.CharField(
        label=Tm_Service._meta.get_field('service_name').verbose_name,
        max_length=Tm_Service._meta.get_field('service_name').max_length,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=True)
    upload_file = forms.FileField(
        label=Tm_Service._meta.get_field('upload_file').verbose_name,
        required=False)

    def __init__(self, *args, **kwargs):
        self.details = kwargs.pop('details') if 'details' in kwargs else None
        super().__init__(*args, **kwargs)

    def clean_upload_file(self):
        infile = self.cleaned_data.get("upload_file")

        if infile is None and not 'file_path' is self.details:
            raise forms.ValidationError('アップロードファイルは必須です。')

        return infile

    def upload_file_save(self):
        infile = self.cleaned_data.get("upload_file")
        if infile:
            tmppath = datetime.now().strftime('upload/temp/%Y%m%d/%H%M%S/')
            url_, path_ = CustomFile.save_file(tmppath + infile.name, infile)

            if self.details and 'file_path' in self.details:
                file_path = self.details['file_path']
                ret = CustomFile.remove_dir(os.path.dirname(file_path))
        else:
            url_ = self.details['file_url']
            path_ = self.details['file_path']
        return (url_, path_)

    def get_upload_file(self):
        infile = self.cleaned_data.get("upload_file")
        tmpfile = None
        if self.details and 'file_path' in self.details:
            file_path = self.details['file_path']
            tmpfile = CustomFile.localfile_to_filefield(file_path)
        return infile if infile else tmpfile      

    # def get_upload_file(self):
    #     # cleaned_data = super(ServiceForm, self).clean()
    #     upload_file = self.cleaned_data.get("upload_file")
        
    #     if upload_file is None and self.details:
    #         file_path = self.details['file_path']
    #         upload_file = CustomFile.localfile_to_filefield(file_path)
    #         if default_storage.exists(file_path):
    #             dirname = os.path.dirname(file_path)
    #             shutil.rmtree(dirname)
    #     return upload_file
