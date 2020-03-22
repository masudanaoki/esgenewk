from django.contrib import admin

# Register your models here.
from . import models

# Register your models here.
@admin.register(models.Tm_Service)
class Tm_ServiceAdim(admin.ModelAdmin):
    list_display = ('id', 'department', 'service_name', 'upload_file', 'order', 'created', 'modified')
    ordering = ('id',)
    fields = ('department', 'service_name', 'upload_file', 'order')

@admin.register(models.Tm_Workflow)
class Tm_WorkflowAdim(admin.ModelAdmin):
    list_display = ('id', 'department', 'workflow_route', 'workflow_count', 'order', 'created', 'modified')
    ordering = ('id',)
    fields = ('department', 'workflow_route', 'workflow_count', 'order')

@admin.register(models.Tm_Authorizer)
class Tm_AuthorizerAdim(admin.ModelAdmin):
    list_display = ('id', 'workflow', 'workflow_count', 'author', 'order', 'created', 'modified')
    ordering = ('id',)
    fields = ('workflow', 'workflow_count', 'author', 'order')

@admin.register(models.Tm_Workflow_Conditions)
class Tm_Workflow_ConditionsAdim(admin.ModelAdmin):
    list_display = ('id', 'workflow', 'service', 'order', 'created', 'modified')
    ordering = ('id',)
    fields = ('workflow', 'service', 'order', 'amount_min', 'amount_max', 'rate_min', 'rate_max')
