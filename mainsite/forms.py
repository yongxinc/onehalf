from django import forms
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):

    acc = forms.CharField(label='使用者帳號', max_length=15)  # 使用者輸入
    pwd = forms.CharField(label='密碼', min_length=6,
                          widget=forms.PasswordInput())
    name = forms.CharField(label='姓名', max_length=30)
    tel = forms.CharField(label='電話', max_length=10)
    mail = forms.EmailField(label='email')
    captcha = CaptchaField(label='機器人驗證')


class LoginForm(forms.Form):
    acc = forms.CharField(label='使用者帳號', max_length=15)  # 使用者輸入
    pwd = forms.CharField(label='密碼', min_length=6,
                          widget=forms.PasswordInput())
