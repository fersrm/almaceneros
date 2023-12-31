from django import forms
from UsuariosStoreApp.models import Usuario
from django.contrib.auth.forms import PasswordChangeForm

# ---------------PERFIL-Usuario-------------


class UsuarioEditarContactoForm(forms.ModelForm):
    telefono_user = forms.CharField(
        label="Teléfono", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Usuario
        fields = ["telefono_user", "email"]


# --------------Cambiar Contraseña-------------


class CambiarContrasenaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("old_password")  # Elimina el campo old_password

    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Usuario
        fields = ["new_password1", "new_password2"]
