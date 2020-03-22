from django.shortcuts import render
from django.template.context_processors import csrf

# from users.models import Tm_Department

from excelapp.forms import forms
from excelapp.models import Tm_Department


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

    # for service in department.Tm_Service_set.all():
    #     print(service)

    return render(request, 'excelapp/index.html')

def multiplechoice(request):
    labels = ['チェック','複数チェック','ラジオボタン','動的選択肢１','動的選択肢２']
    results = {}
    form = ChkForm(request.POST or None)
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
    form = CustommCheckboxForm(request.POST or None)
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
