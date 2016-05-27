#!/usr/bin/env python
#! -*- coding: utf8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
import re

contains = lambda s,xs:any(map(lambda x:x in s, xs))

class RegisterForm(forms.Form):
    email = forms.EmailField(label = u'邮箱',widget = forms.TextInput(attrs = {'size':20}))
    username = forms.CharField(max_length = 20,label = u'用户名',widget = forms.TextInput(attrs = {'size':20}))
    password = forms.CharField(max_length = 20,label = u'密码',widget = forms.PasswordInput())
    re_password = forms.CharField(max_length = 20,label = u'确认密码',widget = forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if contains(username, '.\'"-;'):
            raise forms.ValidationError(u'用户名不能包含 `.\'"-;` 这些特殊字符')
        if User.objects.filter(username = username).count() > 0:
            raise forms.ValidationError(u'这个用户名已经被使用')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('该email已被使用')

    def clean_password(self):
        password = self.cleaned_data['password']
        if contains(password, '.\'"-;'):
            raise forms.ValidationError(u'密码不能包含 `.\'"-;` 这些特殊字符')
        if len(password) >= 6:
            return password
        raise forms.ValidationError('密码至少包含6个字符')

    def clean_re_password(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            re_password = self.cleaned_data['re_password']
            if re_password == password:
                return re_password
        raise forms.ValidationError('两次输入密码不匹配')

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20,required = True,label = u'username')
    password = forms.CharField(max_length = 20,label = u'密码',widget = forms.PasswordInput())
    next = forms.CharField(required = False,widget = forms.HiddenInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if contains(username, '.\'"-;'):
            raise forms.ValidationError(u'用户名不能包含 `.\'"-;` 这些特殊字符')
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        if contains(password, '.\'"-;'):
            raise forms.ValidationError(u'密码不能包含 `.\'"-;` 这些特殊字符')
        if 'username' not in self.cleaned_data:
            return password
        username = self.cleaned_data['username']
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(u'用户名或密码错误')
        self.user = user
        return password