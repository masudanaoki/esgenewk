from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from users.models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(required=False)
    password2 = password1

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):
    CHOICES = (
        ('female', '女性',),
        ('male', '男性',),
        ('not_applicable', '秘密',)
    )
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False)

    def make_select_object(from_x, to_y, dates, increment=True):
        if increment:
            for i in range(from_x, to_y):
                dates.append([i, i])
        else:
            for i in range(from_x, to_y, -1):
                dates.append([i, i])
        return dates

    def make_select_field(select_object):
        dates_field = forms.ChoiceField(
            widget=forms.Select,
            choices=select_object,
            required=False
        )
        return dates_field

    years = [["",""]]
    current_year = datetime.now().year
    years = make_select_object(current_year, current_year-80, years, increment=False)
    birth_year = make_select_field(years)

    months = [["",""]]
    months = make_select_object(1, 13, months)
    birth_month = make_select_field(months)

    days = [["",""]]
    days = make_select_object(1, 32, days)
    birth_day = make_select_field(days)

    class Meta:
        model = Profile
        fields = ('gender', 'birth_year', 'birth_month', 'birth_day')
