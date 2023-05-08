from django import forms
from accounts.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, help_text="super_vanya", label="Псевдоним")
    first_name = forms.CharField(max_length=50, help_text="Иван", label="Имя")
    last_name = forms.CharField(max_length=50, help_text="Иванов", label="Фамилия")
    email = forms.EmailField(max_length=254, help_text="ivan.ivanov@mail.ru", label="Почта")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    repeat_password = forms.CharField(widget=forms.PasswordInput, label="Повтор пароля")
    avatar = forms.ImageField(required=False, label="Аватар")

    def clean_username(self):  # пробелы
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this nickname already exists!")
        if ' ' in username:
            raise forms.ValidationError("Username cannot contain spaces!")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("Name must consists only by letters!")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Surname must consists only by letters!")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar is None:
            return
        avatar.name = f"{self.cleaned_data['username']}_avatar"
        return avatar

    def clean(self):
        passwd = self.cleaned_data['password']
        repeat = self.cleaned_data['repeat_password']
        if passwd != repeat:
            raise forms.ValidationError("Passwords aren't the same!")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Псевдоним")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")

    # def clean(self):
    #     return self.cleaned_data


class SettingsForm(forms.Form):
    username = forms.CharField(required=False, max_length=50)
    first_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=False, max_length=50)
    email = forms.EmailField(required=False, max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    avatar = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this nickname already exists!")
        if ' ' in username:
            raise forms.ValidationError("Username cannot contain spaces!")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("Name must consists only by letters!")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Surname must consists only by letters!")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        return avatar

    def clean(self):
        passwd = self.cleaned_data['password']
        return self.cleaned_data
