from django import template

register = template.Library()

# カスタムタグとして登録する
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