from django import forms

from core.user.models import User


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Usuario')

    def clean(self):
        cleaned = super().clean()
        users = User.objects.filter(username=cleaned['username'])
        if not users.exists():
            raise forms.ValidationError('El username no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Password')

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita el password',
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Confirmación de password')

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirm_password = cleaned['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned
