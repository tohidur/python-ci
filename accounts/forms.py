from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django import forms

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Email')
    #username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # user = authenticate(username=username, password=password)
            user = None
            user_qs = User.objects.filter(username=username)
            if user_qs.count() == 1:
                user = user_qs.first()
            if not user:
                raise forms.ValidationError("This user doesn't exists")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Name')
    #email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            #'last_name',
            #'email',
            #'email2',
            'password',
        ]

    def clean_email2(self):
        email = self.cleaned_data.get('username')
        # email2 = self.cleaned_data.get('email2')
        # if email != email2:
        #     raise forms.ValidationError('Email must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email already been registered')
        return email
