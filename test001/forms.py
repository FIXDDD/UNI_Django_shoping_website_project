from django import forms
from django.contrib.auth.models import User
from test001.models import Customer, Products
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator # check db Characters
from collections import OrderedDict     # To order dictionary

import re  # To validate password



# B1 Register form
# https://overiq.com/django-1-10/django-creating-users-using-usercreationform/
class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    first_name = forms.CharField(label='Enter First Name', max_length=150)
    last_name = forms.CharField(label='Enter Last Name', max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', min_length=5)
    password2 = forms.CharField(label='Confirm password', min_length=5)
    address = forms.CharField(max_length=255)

    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # B3: validate password
        check = re.search(r'\d.*[A-Z]|[A-Z].*\d', password1)
        check1 = len(password1) >= 6
        if not check:
            raise forms.ValidationError(
                "Password needs to contain at least one uppercase letter and at least one number."
            )
        if not check1:
            raise forms.ValidationError(
                "Password needs to contain at least 6 character."
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match with previous entered password!")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        user.save()
        search = User.objects.get(username=self.cleaned_data['username']).id
        customer = Customer.objects.get(Cust_iD=search)
        customer.Address = self.cleaned_data['address']
        customer.save()
        return user


# B2: customer login form
class customer_login(forms.ModelForm):
    username = forms.CharField(max_length=150, label='User Name')
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'password')


# B3: customer change password form
class customer_change_pw(forms.Form):
    old_password = forms.CharField(label='Current Password', min_length=5)
    new_password1 = forms.CharField(label='New Password', min_length=5)
    new_password2 = forms.CharField(label='Enter new Password again', min_length=5)

    def clean_old_password(self):
        password = self.cleaned_data.get('old_password')

        # B3: validate password
        check = re.search(r'\d.*[A-Z]|[A-Z].*\d', password)
        check1 = len(password) >= 6
        if not check:
            raise forms.ValidationError(
                "Password needs to contain at least one uppercase letter and at least one number."
            )
        if not check1:
            raise forms.ValidationError(
                "Password needs to contain at least 6 character."
            )
        return password

    def clean_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # B3: validate password
        check = re.search(r'\d.*[A-Z]|[A-Z].*\d', password1)
        check1 = len(password1) >= 6
        if not check:
            raise forms.ValidationError(
                "Password needs to contain at least one uppercase letter and at least one number."
            )
        if not check1:
            raise forms.ValidationError(
                "Password needs to contain at least 6 character."
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2
