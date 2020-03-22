from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from users.models import *

User = get_user_model()


# Create your models here.
class Tm_Service(BaseModel):
    department = models.ForeignKey(Tm_Department, on_delete=models.PROTECT, related_name='services', verbose_name ='部門')
    service_name = models.CharField(max_length=200, verbose_name ='サービス名')
    upload_file = models.FileField(null=True, blank=True, upload_to='upload', verbose_name ='アップロードファイル')
    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'Tm_Service'
        verbose_name ='サービスマスタ'
        verbose_name_plural = 'サービスマスタ'

class Tm_Workflow(BaseModel):
    WORKFLOW_ROUTE = (
        (1, '通常'),
        (2, '特別'),
    )
    department = models.ForeignKey(Tm_Department, on_delete=models.PROTECT, verbose_name ='部門')
    workflow_route = models.IntegerField(choices=WORKFLOW_ROUTE, default='1', verbose_name ='承認経路')
    workflow_count = models.IntegerField(default=1, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(3)], verbose_name ='承認回数')
    def __str__(self):
        return self.department.department_name  + ',' + self.get_workflow_route_display()

    class Meta:
        db_table = 'Tm_Workflow'
        verbose_name ='承認マスタ'
        verbose_name_plural = '承認マスタ'

class Tm_Authorizer(BaseModel):
    workflow = models.ForeignKey(Tm_Workflow, on_delete=models.PROTECT, verbose_name ='承認')
    workflow_count = models.IntegerField(default=1, verbose_name ='承認回数')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name ='承認者')
    def __str__(self):
        return self.author.username

    class Meta:
        db_table = 'Tm_Authorizer'
        verbose_name ='承認者マスタ'
        verbose_name_plural = '承認者マスタ'

class Tm_Workflow_Conditions(BaseModel):
    workflow = models.ForeignKey(Tm_Workflow, on_delete=models.PROTECT, verbose_name ='承認')
    service = models.ForeignKey(Tm_Service, on_delete=models.PROTECT, verbose_name ='サービス')
    amount_min = models.IntegerField(null=True, blank=True, verbose_name ='金額（下限）')
    amount_max = models.IntegerField(null=True, blank=True, verbose_name ='金額（上限）')
    rate_min = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1, verbose_name ='利益率（下限）')
    rate_max = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1, verbose_name ='利益率（上限）')
    def __str__(self):
        return self.workflow.department.department_name  + ',' + self.workflow.get_workflow_route_display()

    class Meta:
        db_table = 'Tm_Workflow_Conditions'
        verbose_name ='承認経路条件マスタ'
        verbose_name_plural = '承認経路条件マスタ'
