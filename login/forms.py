from django import forms
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from .models import UserProfile



class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    captcha = ReCaptchaField(
        public_key='6LfXW7YpAAAAAL8jK1aqM3tTxmboCldcv_ArBuke',
        private_key='6LfXW7YpAAAAAE4p3o045ydI1n6KJTgTFJom4v1M',
        widget=ReCaptchaV3(
        action='signup',
        attrs={
            'required_score':0.85,
        }
    )
    )
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tài khoản đã tồn tại")
        return username     

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email đã tồn tại") 
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu không khớp")
        return password2

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user


class UserLoginForm(forms.Form):
    username_login = forms.CharField(label='Tài khoản', max_length=30)
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    captcha = ReCaptchaField(
        public_key='6Le7X7YpAAAAAGxRFI8KF1eZ3Wu7klBIRUVzKwPS',
        private_key='6Le7X7YpAAAAADsC48wG0R5Y7PJ4VmTyzJkOHYyI',
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mota', 'vitri', 'birth_date', 'nickname', 'avatar', 'account_name', 'additional_info']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            initial_data = {
                'account_name': self.user.username if self.user.username else '',  # Sử dụng tên tài khoản nếu có, ngược lại để trống
                'email': self.user.email if self.user.email else '',  # Sử dụng email nếu có, ngược lại để trống
            }
            self.initial.update(initial_data)

    def save(self, commit=True):
        instance = super(UserProfileForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
            if commit:
                instance.save()
        return instance

        