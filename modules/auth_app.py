from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.conf import settings

from user.forms import ProfileForm
from user.models import Profile
from .code import id_generate
import re, time

class PhoneObject:
    def __init__(self, phone):
        self.phone = phone
        self.error_status = False
        self.error_msg = ''

    def clean_phone(self):
        phone = self.phone
        
        # remove hyphen
        if '-' in phone:
            phone = ''.join(phone.split('-'))
        # remove space
        if ' ' in phone:
            phone = ''.join(phone.split(' '))

        if phone[0] == '+':
            return phone
        elif phone[:2] == '88':
            return '+' + phone
        else:
            return '+88' + phone

    def is_valid(self):
        phone = self.phone

        # for bd
        operator = ['11', '15', '16', '18', '17', '13', '19', '14',]

        # check if start char is ok
        if phone[0] not in ['+', '8', '0']:
            self.error_status = True
            self.error_msg = 'Invalid Phone Number.'
            return

        # clean number
        phone = self.clean_phone()

        # check length
        if len(phone) != 14:
            self.error_status = True
            self.error_msg = 'Invalid Phone Number.'
            return

        # check if phone number exists
        phone = phone[1:]
        pattern = re.compile(r'(880)(\d{2})(\d{8})')
        phone_group = pattern.findall(phone)
        if len(phone_group) == 0:
            self.error_status = True
            self.error_msg = 'Invalid Phone Number.'
            return
        
        # check valid opearator
        phone_group = list(pattern.findall(phone)[0])
        if phone_group[1] not in operator:
            self.error_status = True
            self.error_msg = 'Invalid Phone Number.'
            return

        self.phone = '+' + phone
        return

class EmailObject:
    def __init__(self, email):
        self.email = email
        self.error_status = False
        self.error_msg = ''
    
    def is_valid(self):
        f = forms.EmailField()
        try:
            f.clean(self.email)
            self.error_status = False
            return
        except Exception as e:
            # print(str(e))
            self.error_msg = 'Email is not valid.'
            self.error_status = True
            return

    def exists(self, mode=None):
        obj = User.objects.filter(email=self.email)

        if mode == 'register':
            if len(obj) >= 1:
                self.error_status = True
                self.error_msg = 'Email exists.'
        elif mode == 'login':
            if len(obj) == 0:
                self.error_status = True
                self.error_msg = 'Email does not exist.'
        return

class PasswordObject:
    def __init__(self, password):
        self.password = password
        self.error_status = False
        self.error_msg = ''

    def is_valid(self):
        if len(self.password) < 8:
            self.error_msg = 'Password must be at least 8 characters long.'
            self.error_status = True
            return
        if self.password.isdigit():
            self.error_msg = 'Password is fully Numeric.'
            self.error_status = True
            return
        if self.password.isalpha():
            self.error_msg = 'Password is fully Alphabetic.'
            self.error_status = True
            return
        
        return

    def is_match(self, confirm):
        if self.password != confirm:
            self.error_status = True
            self.error_msg = 'Password did not match.'
            return
        return

class NameObject:
    def __init__(self, name):
        self.name = name
        self.error_status = False
        self.error_msg = ''

    def is_valid(self):
        if len(self.name) < 2:
            self.error_msg = 'Name must be at least 2 characters long.'
            self.error_status = True
            return
        
        pattern = re.compile(r'^[a-zA-z. ]{2,}$')
        search = pattern.findall(self.name)
        if len(search) != 1:
            self.error_msg = 'Name can only contain A-Z, a-z, dot, space.'
            self.error_status = True
            return
        return

class RegisterObject(object):
    def __init__(self, request):
        self.request = request
        self.user_cleared = False
        self.error_status = False
        self.msg = ''
        self.user_obj = None
        self.profile_obj = None

        if request.user.is_authenticated:
            self.user = request.user
            self.is_authenticated = True
        else:
            self.user = None
            self.is_authenticated = False

    def get_user_data(self):
        try:
            self.first_name = self.request.POST['first_name']
            self.last_name = self.request.POST['last_name']
            self.institute = self.request.POST['institute']
            self.email = self.request.POST['email']
            self.phone = self.request.POST['phone']
            self.address = self.request.POST['address']
            self.password = self.request.POST['password']
            self.confirm = self.request.POST['confirm']
        except:
            self.error_status = True
            self.msg = 'Enter valid data.'

    def validate_user_data(self):
        first_name_obj = NameObject(self.first_name)
        first_name_obj.is_valid()
        if first_name_obj.error_status:
            self.msg = first_name_obj.error_msg
            self.error_status = True
            return
        
        last_name_obj = NameObject(self.last_name)
        last_name_obj.is_valid()
        if last_name_obj.error_status:
            self.msg = last_name_obj.error_msg
            self.error_status = True
            return

        email_obj = EmailObject(self.email)
        email_obj.is_valid()
        if email_obj.error_status:
            self.msg = email_obj.error_msg
            self.error_status = True
            return

        email_obj.exists(mode='register')
        if email_obj.error_status:
            self.msg = email_obj.error_msg
            self.error_status = True
            return

        phone_obj = PhoneObject(self.phone)
        phone_obj.is_valid()
        if phone_obj.error_status:
            self.msg = phone_obj.error_msg
            self.error_status = True
            return
        self.phone = phone_obj.phone

        pass_obj = PasswordObject(self.password)
        pass_obj.is_valid()
        if pass_obj.error_status:
            self.msg = pass_obj.error_msg
            self.error_status = True
            return

        pass_obj.is_match(self.confirm)
        if pass_obj.error_status:
            self.msg = pass_obj.error_msg
            self.error_status = True
            return

        return

    def create_user(self):
        try:
            user_obj = User(username=id_generate(), email=self.email)
            user_obj.set_password(self.password)
            user_obj.save()
            self.user_obj = user_obj
        except Exception as e:
            print(e)
            self.msg = 'Error occured.'
            self.error_status = True
        return

    def create_profile(self):
        try:
            data = {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'institute': self.institute,
                'phone': self.phone,
                'address': self.address,
            }
            form = ProfileForm(data)
            if form.is_valid():
                profile_obj = form.save(commit=False)
                profile_obj.user = self.user_obj
                profile_obj.save()
                self.profile_obj = profile_obj
            else:
                self.msg = 'Error occured.'
                self.error_status = True
        except Exception as e:
            print(e)
            self.msg = 'Error occured.'
            self.error_status = True
        return

    def create(self):
        try:
            self.get_user_data()
            if not self.error_status:
                self.validate_user_data()
            else:
                return

            if not self.error_status:
                self.create_user()
            else:
                return
            
            if not self.error_status:
                self.create_profile()
            else:
                return
            
            if self.error_status:
                raise Exception
            self.msg = 'Success!\nLog In To Continue!'

        except Exception as e:
            print(e)
            self.clean()
            self.msg = 'Error occured.'
            self.error_status = True
        return

    def clean(self):
        if not self.user_obj is None:
            self.user_obj.delete()
        return

class AuthObject:
    def __init__(self, request):
        self.request = request
        self.error_status = False
        self.msg = ''

        try:
            self.email = request.POST['email']
            self.password = request.POST['password']
        except:
            self.error_status = True
            self.msg = 'Enter valid data.'

        if request.user.is_authenticated:
            self.user = request.user
            self.is_authenticated = True
        else:
            self.user = None
            self.is_authenticated = False
    
    def log_in(self):
        email_obj = EmailObject(self.email)
        email_obj.is_valid()
        if email_obj.error_status:
            self.msg = email_obj.error_msg
            self.error_status = True
            return

        email_obj.exists(mode='login')
        if email_obj.error_status:
            self.msg = email_obj.error_msg
            self.error_status = True
            return
        
        try:
            username = User.objects.get(email=self.email)
            login(self.request, authenticate(self.request, username=username, password=self.password))
            self.msg = 'Welcome back!'
            return
        except Exception as e:
            # print(str(e))
            self.error_status = True
            self.msg = 'Log in failed!\nCheck your password.'
            return

    def log_out(self):
        try:
            logout(self.request)
            return
        except Exception as e:
            self.error_status = True
            self.msg = 'Logout failed.'
            return
