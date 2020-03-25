from django.urls import path
from excelapp.views import views, upload

app_name = 'excelapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('multiplechoice/', views.multiplechoice, name='multiplechoice'),
    path('custumfilter/', views.custumfilter, name='custumfilter'),
    path('customcheckboxselectmultiple/', views.customcheckboxselectmultiple, name='customcheckboxselectmultiple'),
    path('bootstrap/', views.bootstrap, name='bootstrap'),
    path('bootstrapimage/', views.bootstrapimage, name='bootstrapimage'),
    path('bootstrapcomponents/', views.bootstrapcomponents, name='bootstrapcomponents'),
    path('bootstrapform/', views.bootstrapform, name='bootstrapform'),

    path('upload/', upload.ServiceList.as_view(), name='upload_List'),
    path('upload/input/', upload.input, name='upload_input'),
    path('upload/update/<int:pk>/', upload.update, name='upload_update'),
    path('upload/confirm/', upload.confirm, name='upload_confirm'),   
    path('upload/create/', upload.create, name='upload_create'),  
]
