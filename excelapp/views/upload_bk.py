import getpass
import io
import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from excelapp.forms.upload import ServiceForm
from excelapp.models import Tm_Department, Tm_Service
from excelapp.utils.base64_util import CustomBase64
from excelapp.utils.file_util import CustomFile

User = get_user_model()
def index(request):
    return render(request, 'excelapp/upload/index.html')


class ServiceList(generic.ListView):
    template_name = 'excelapp/upload/list.html'
    model = Tm_Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        if 'details' in self.request.session:
            del self.request.session['details']
        return context


def input(request):
    details = request.session.get('details', None)
    if request.method == 'GET':
        initial = {}
        if details and 'form_data' in details:
            form_data = details['form_data']
            initial['department'] = form_data['department']
            initial['service_name'] = form_data['service_name']
       
        form = ServiceForm(None, initial=initial, details=details)
    else:
        form = ServiceForm(data=request.POST, files=request.FILES, details=details)
        if form.is_valid():
            # infile = form.get_upload_file()        
            # infile_value = infile.file.getvalue()
            # enc_file = CustomBase64.encode_str(infile_value)

            file_url, file_path = form.upload_file_save()
            details = {}
            details['form_data'] = request.POST
            details['file_url'] = file_url
            details['file_path'] = file_path
            # details['upload_file_data'] = enc_file
            request.session['details'] = details
            return redirect('excelapp:upload_confirm')
    context = {
        'form': form
    }
    if details:
        context['file_url'] = details['file_url']
        context['file_path'] = details['file_path']

    return render(request, 'excelapp/upload/input.html', context)

def confirm(request):
    details = request.session.get('details', None)
    if details is None:
        return redirect('excelapp:upload_input')
    form_data = details['form_data']
    file_url = details['file_url']

    context = {
        'form': ServiceForm(form_data),
        'uploadfile_url': file_url,
    }
    return render(request, 'excelapp/upload/confirm.html', context)

def create(request):
    details = request.session.pop('details', None)
    if details is None:
        return redirect('excelapp:upload_input')

    form_data = details['form_data']
    file_url = details['file_url']
    file_path = details['file_path']
    # upload_file_data = details['upload_file_data']

    tm_service = Tm_Service()
    tm_service.department = Tm_Department.objects.get(pk=form_data['department']) 
    tm_service.service_name = form_data['service_name']
    data = CustomFile.localfile_to_filefield(file_path)
    # sdata = CustomBase64.decode(upload_file_data)
    # sdata = io.BytesIO(sdata)
    # sdata.seek(0)
    # sdata = ContentFile(sdata.getvalue())
    # sdata.name = os.path.basename(file_path)
    # tm_service.upload_file = sdata
    tm_service.upload_file = data
    tm_service.save()
    ret = CustomFile.remove_dir(os.path.dirname(file_path))

    # #クリア
    # request.session.clear()
    # #セッション&クッキー 削除
    # request.session.flush()

    return redirect('excelapp:upload_List')
