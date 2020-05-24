# from users.models import Tm_Department
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render
from django.template.context_processors import csrf

from excelapp.forms import forms
from excelapp.forms.formset import ServiceCreateForm, ServiceCreateFormSet, ServiceForm
from excelapp.models import Tm_Department, Tm_Service


# Create your views here.
def index(request):
    # services = Tm_Service.objects.filter(department__department_name='モニタリング')
    # for service in services:
    #     print(service)

    # departments = Tm_Department.objects.filter(department_name='モニタリング')
    # for department in departments:
    #     print(department)
    
    # for service in departments[0].services.all():
    #     print(service)

    department = Tm_Department.objects.get(pk=1)




    for service in department.services.all():
        print(service)


    map_list = map(lambda x: x.service_name, Tm_Service.objects.all())
    list_ = list(map_list)
    print(list_)

    map_list1 = map(_get_service_name, Tm_Service.objects.all())
    list_1 = list(map_list1)
    print(list_1)

    map_list2 = map(lambda x: x.department_name, filter(lambda x: x.department_name == '部門Ａ', Tm_Department.objects.all()))
    list_2 = list(map_list2)
    print(list_2)




    # for service in department.Tm_Service_set.all():
    #     print(service)

    return render(request, 'excelapp/index.html')

def _get_service_name(tm_service):
    return tm_service.service_name


def multiplechoice(request):
    labels = ['チェック','複数チェック','ラジオボタン','動的選択肢１','動的選択肢２']
    results = {}
    form = forms.ChkForm(request.POST or None)
    choice1 = []
    choice1.append(('1','動的選択肢１'))
    choice1.append(('2','動的選択肢２'))
    choice1.append(('3','動的選択肢３'))
    choice1.append(('4','動的選択肢４'))
    form.fields['four'].choices = choice1
    form.fields['five'].choices = choice1

    if request.method == 'POST':
        results[labels[0]] = request.POST.getlist("one")
        results[labels[1]] = request.POST.getlist("two")
        results[labels[2]] = request.POST.getlist("three")
        results[labels[3]] = request.POST.getlist("four")
        results[labels[4]] = request.POST.getlist("five")
    else:
        form.fields['four'].initial = ['2']
        form.fields['five'].initial = ['3']
        # CFRF対策（必須）
        # c.update(csrf(request))
    context = {
            'form': form,
            }
    return render(request, 'excelapp/checkboxselectmultiple.html', context)

def custumfilter(request):
    departments = Tm_Department.objects.all()
    department = Tm_Department.objects.get(pk=1)
    context = {
            'departments': departments,
            'department1': department,
            }
    return render(request, 'excelapp/custumfilter.html', context)

def customcheckboxselectmultiple(request):
    results = {}
    form = forms.CustommCheckboxForm(request.POST or None)
    if request.method == 'POST':
        results['service'] = request.POST.getlist("service")
    else:
        pass
    context = {
            'form': form,
            }
    return render(request, 'excelapp/customcheckboxselectmultiple.html', context)

def bootstrap(request):
    context = {
            }
    return render(request, 'excelapp/bootstrap.html', context)

def bootstrapimage(request):
    context = {
            }
    return render(request, 'excelapp/bootstrapimage.html', context)

def bootstrapcomponents(request):
    context = {
            }
    return render(request, 'excelapp/bootstrapcomponents.html', context)

def bootstrapform(request):
    context = {
            }
    return render(request, 'excelapp/bootstrapform.html', context)

def formset(request):

    serviceformset = formset_factory(
            form=ServiceForm,
            extra=0,
    )
    tm_service = Tm_Service.objects.all()
    services = []
    for service in tm_service:
        service_dict = {
            'pk': service.pk,
            'x': service.pk,
            'department_name': service.department.department_name,
            'service_name': service.service_name,
        }
        services.append(service_dict)
    
    dict_ = {'form-0-delete_check': 'on'}
    if request.method == 'GET':
        formset = serviceformset(None, initial=services)
    else:
        formset = serviceformset(request.POST, initial=services) 

    # serviceformset = modelformset_factory(
    #         model=Tm_Service,
    #         form=ServiceCreateForm,
    #         extra=0,
    # )
    # if request.method == 'POST':
    #     formset = serviceformset(request.POST, queryset=Tm_Service.objects.all()) 
    # else:
    #     formset = serviceformset(None, queryset=Tm_Service.objects.all())

    context = {
        'formset': formset,
        'tm_service': tm_service,
    }
    return render(request, 'excelapp/formsetlist.html', context)

    # formset = ServiceCreateFormSet(request.POST or None)
    # if request.method == 'POST' and formset.is_valid():
    #     # formset.save()
    #     # return redirect('app:index')
    #     print(formset)

    # context = {
    #     'formset': formset
    # }

    # return render(request, 'excelapp/formsetlist.html', context)

def rest(request):
    context = {
            }
    return render(request, 'excelapp/rest.html', context)
