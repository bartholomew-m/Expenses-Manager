from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.core import validators

from expenses_manager.models import ExpenseCategory, Tag


class LoginForm(forms.Form):
    """
    Form for expenses manager login
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned = super().clean()
        user = authenticate(username=cleaned['username'], password=cleaned['password'])
        if not user:
            raise ValidationError('Invalid credentials')
        return cleaned


class CreateAccountForm(forms.Form):
    """
    Form for creating user account
    """
    name = forms.CharField(validators=[validators.MaxLengthValidator(100)])
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(),
        validators=[validators.MaxLengthValidator(500)]
    )


class CreateWalletForm(forms.Form):
    """
    Form for account wallet
    """
    name = forms.CharField(validators=[validators.MaxLengthValidator(100)])
    tags = forms.ModelMultipleChoiceField(required=False, queryset=Tag.objects.all())


class CreateExpenseForm(forms.Form):
    """
    Add expense to wallet form
    """
    category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.all())
    name = forms.CharField(validators=[validators.MaxLengthValidator(100)])
    amount = forms.DecimalField()
    description = forms.CharField(required=False, widget=forms.Textarea, validators=[validators.MaxLengthValidator(500)])
    pin = forms.BooleanField(required=False)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=Tag.objects.all())


class DeleteExpenseForm(forms.Form):
    """
    Delete expense form
    """
    expense_pk = forms.IntegerField(widget=forms.HiddenInput)
