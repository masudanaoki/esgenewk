import os

from django import template
from django.utils.safestring import mark_safe

from excelapp.models import Tm_Service

register = template.Library()

@register.simple_tag
def add_attr(field, *args, **attr):
    print(field)
    if field:
        field.field.widget.attrs.update(attr)
        if 'class' in field.field.widget.attrs:
            if field.form.is_bound:
                if field.errors:
                    field.field.widget.attrs['class'] += ' is-invalid'
                else:
                    field.field.widget.attrs['class'] += ' is-valid'
        print(field.field.widget.attrs)
    return field

@register.simple_tag
def file_link(url, file):
    return mark_safe(f'<a href="{url}" class="" download="{os.path.basename(file)}">{os.path.basename(file)}</a>')

@register.inclusion_tag('excelapp/customtag/service_list.html')
def create_service_list():
    tm_service = Tm_Service.objects.all()
    return {'tm_service': tm_service}

@register.inclusion_tag('excelapp/customtag/file_change.html')
def create_file_change(field, file_url=None, file_path=None):
    return {'field': field, 'file_url': file_url, 'file_path': file_path}
