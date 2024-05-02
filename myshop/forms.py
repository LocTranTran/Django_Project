from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Tên Tài Khoản',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial=''
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        initial=''
    )
    password1 = forms.CharField(
        label='Mật Khẩu',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        initial=''
    )
    password2 = forms.CharField(
        label='Nhập Lại Mật Khẩu',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        initial=''
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Tên tài khoản đã được sử dụng!')
        return username

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError('Email đã được đăng ký. Vui lòng sử dụng một cái khác.')
    #     return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            error_message = 'Vui lòng nhập cùng một mật khẩu vào cả hai trường.'
            self.add_error('password2', error_message)

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        # Tạo khách hàng mới và liên kết người dùng với khách hàng
        customer = Customer.objects.create(user=user)
        customer.name = username  # Cập nhật tên của khách hàng
        customer.save()
        return user
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Tên Tài Khoản',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial=''
    )
    password1 = forms.CharField(
        label='Mật Khẩu',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        initial=''
    )

# Tìm kiếm sản phẩm 
class ProductSearchForm(forms.Form):
    search_item = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control rounded-0 search-input', 'placeholder': 'Nhập tên sản phẩm'}))
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
                
class ReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'review-comment'}))

    class Meta:
        model = Review
        fields = ['rating', 'comment', 'image']