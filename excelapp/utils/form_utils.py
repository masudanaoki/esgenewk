from django.forms.utils import ErrorList

class FormUtil():
    def append_validation_error(form, field_name, message):
        error_list = form.errors.get(field_name)
        if error_list is None:
            error_list = ErrorList()
            form.errors[field_name] = error_list
        error_list.append(message)

