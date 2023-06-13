from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from apps.recibo.models import DatosAdicionales


class LoginForm(forms.Form):
    username = forms.CharField(
        validators= [RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$', message= "El usuario no debe contener números")],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Clave",
                "class": "form-control",
                'autocomplete': 'off'
            }
        ))

class SignUpForm(UserCreationForm):
    password2 = None
    email = None

    class Meta:
        model = User
        fields = ('username', 'password1')

class EditForm(forms.ModelForm):
    class Meta:
        model = DatosAdicionales
        fields = ['nombre','apellido','documento','email','telefono']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['nombre'].widget.attrs['readonly'] = True
        self.fields['apellido'].widget.attrs['readonly'] = True
        self.fields['documento'].widget.attrs['readonly'] = True

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class':'form-control form-control-sm'})

class EditPassForm(forms.Form):

    oldpassword = forms.CharField(
    label = 'Contraseña actual',
    widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            'autocomplete': 'off'
        }
    ))

    password1 = forms.CharField(
    label='Contraseña nueva',
    widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            'autocomplete': 'off'
        }
    ))

    password2 = forms.CharField(
    label= 'Repetir contraseña nueva',
    widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            'autocomplete': 'off'
        }
    ))

    # Valida que las contraseñas 1 y 2 coincidan
    def clean_password2(self):
        oldpassword = self.cleaned_data.get('oldpassword')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if oldpassword == password1:
            raise forms.ValidationError('La nueva contraseña debe ser distinta a la contraseña actual')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')

