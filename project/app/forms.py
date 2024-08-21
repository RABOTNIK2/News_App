from .models import *
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm, UserCreationForm, SetPasswordMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, password_validation
from captcha.fields import CaptchaField, CaptchaTextInput

class PersonCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'image', 'is_staff', 'age', 'is_superuser')

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class PersonChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'name', 'age', 'image', 'password', 'is_active', 'is_superuser',)

    def clean_password(self):
        return self.initial["password"]
    
class PasswordMixin:
    error_messages = {
        "password_mismatch": _("Пароли не совпадают"),
    }

    @staticmethod
    def create_password_fields(label1=_("Пароль"), label2=_("Подтвердите пароль")):
        password1 = forms.CharField(
            label=label1,
            required=False,
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        )
        password2 = forms.CharField(
            label=label2,
            required=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            strip=False,
        )
        return password1, password2


    def validate_passwords(
        self,
        password1_field_name="password1",
        password2_field_name="password2",
        usable_password_field_name="usable_password",
    ):
        usable_password = (
            self.cleaned_data.pop(usable_password_field_name, None) != "false"
        )
        self.cleaned_data["set_usable_password"] = usable_password
        password1 = self.cleaned_data.get(password1_field_name)
        password2 = self.cleaned_data.get(password2_field_name)

        if not usable_password:
            return self.cleaned_data

        if not password1 and password1_field_name not in self.errors:
            error = ValidationError(
                self.fields[password1_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password1_field_name, error)

        if not password2 and password2_field_name not in self.errors:
            error = ValidationError(
                self.fields[password2_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password2_field_name, error)

        if password1 and password2 and password1 != password2:
            error = ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
            self.add_error(password2_field_name, error)

    def validate_password_for_user(self, user, password_field_name="password2"):
        password = self.cleaned_data.get(password_field_name)
        if password and self.cleaned_data["set_usable_password"]:
            try:
                password_validation.validate_password(password, user)
            except ValidationError as error:
                self.add_error(password_field_name, error)

    def set_password_and_save(self, user, password_field_name="password1", commit=True):
        if self.cleaned_data["set_usable_password"]:
            user.set_password(self.cleaned_data[password_field_name])
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    
class UserRegisterForm(PasswordMixin ,forms.ModelForm):

    name = forms.CharField(max_length=60, label=_('Имя'), widget=forms.TextInput(attrs={
        'placeholder': 'Введите ваше имя',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    email = forms.EmailField(label=_("Электронная почта"), max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': 'Введите ваш email',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    password1, password2 = PasswordMixin.create_password_fields()
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("email", "name")



    def clean(self):
        self.validate_passwords()
        return super().clean()

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        self.validate_password_for_user(self.instance)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
            self.fields['name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'password123'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'password123'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})

class UserLoginForm(forms.Form):

    email = forms.EmailField(label=_("Почта"), max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': 'Введите ваш email',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Пожалуйста введите правильную почту или пароль "
            "fields may be case-sensitive."
        ),
        "inactive": _("Аккаунт не активирован"),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['email'].widget.attrs['placeholder'] = 'Почта пользователя'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
            self.fields['email'].label = 'Почта'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )

    
class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'age')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class ChangePicture(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', )

    image = forms.ImageField(label=_("Фото ебать"), widget=forms.FileInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)

    comment_text = forms.CharField(max_length=5000, label=_('Напишите ваше мнение'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
