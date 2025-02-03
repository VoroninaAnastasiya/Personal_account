from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction

from .models import User, ProfileUser, UserImage


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='password')
    password2 = forms.CharField(label='password')

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        print(user)
        user.set_password(self.cleaned_data['password1'])
        print(user.password)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='email', max_length=254)
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        #model = get_user_model()
        model = User
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Неверный логин или пароль")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    date_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                 label='Дата рождения')
    image = forms.ImageField(required=False)
    class Meta:
        model = ProfileUser
        fields = ['first_name', 'date_birth', 'info_about_user', 'user', 'image']

    def save(self, commit=True):
        profile = super().save()
        print('+++++', self.cleaned_data)
        print(profile)
        image = self.cleaned_data.get('image')
        print(image)
        if image is not None:
            new_image = UserImage.objects.create(image=image, user_profile=profile)
            print(new_image)
        return profile




