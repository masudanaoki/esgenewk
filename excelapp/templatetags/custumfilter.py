from django import template

register = template.Library()

@register.filter
def padding0(value, num):
    # formatstr = '{{:0{}}}'.format(num)
    # return formatstr.format(value)

    # return format(value, '0{}'.format(num))
    return f'{{:0{num}}}'.format(value)

    # return f'{value:03}'
    # return str(value).zfill(num)

@register.filter
def num_delimiter(value):
    return '{:,}'.format(int(value))
