from django.db.models.query import QuerySet
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from expenses_manager.models import Account, Expense, Wallet
from expenses_manager.forms import CreateAccountForm, CreateExpenseForm, CreateWalletForm, DeleteExpenseForm, LoginForm
from expenses_manager.permissions import IsAccountOwner, IsLoggedIn


def logout_view(request):
    """
    Logout view
    """
    logout(request)
    return redirect('login')


class LoginView(FormView):
    """
    Login view
    """
    template_name = 'login-view.html'
    form_class = LoginForm
    success_url = '/expenses-manager/home'

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Login user when form is valid
        """
        login(self.request, User.objects.get(username=form.cleaned_data['username']))
        return super().form_valid(form)


class HomeView(IsLoggedIn, ListView):
    """
    Home view.
    Restricted to logged in users.
    """
    template_name = 'home-view.html'
    model = Account
    context_object_name = 'accounts'

    def get_queryset(self) -> QuerySet:
        """
        Filer context based on request.user
        """
        return self.model.objects.filter(user=self.request.user)


class CreateAccountView(IsLoggedIn, FormView):
    """
    Create new account view.
    Restricted to logged in users.
    """
    template_name = 'create-account-view.html'
    form_class = CreateAccountForm
    success_url = '/expenses-manager/home'

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Create new account when form is valid
        """
        account = Account(
            user=self.request.user,
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description']
        )
        account.save()
        return super().form_valid(form)


class AccountDetailsView(IsAccountOwner, DetailView):
    """
    Account details view.
    Restricted to account owners (logged in user must be account owner).
    """
    template_name = 'account-details-view.html'
    model = Account
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        """
        Filter context based on account
        """
        context = super().get_context_data(**kwargs)
        context['wallets'] = Wallet.objects.filter(account=self.get_object())
        return context


class CreateWalletView(IsAccountOwner, FormView):
    """
    Create new account wallet view.
    Restricted to account owners (logged in user must be account owner).
    """
    template_name = 'create-wallet-view.html'
    form_class = CreateWalletForm

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Create new account when form is valid
        """
        wallet = Wallet(
            name=form.cleaned_data['name'],
            account=Account.objects.get(pk=self.kwargs['account_pk'])
        )
        wallet.save()
        wallet.tags.set(form.cleaned_data['tags'])
        self.success_url = wallet.get_absolute_url()
        return super().form_valid(form)


class WalletDetailsView(IsAccountOwner, DetailView):
    """
    Wallet details view.
    Restricted to account owners (logged in user must be account owner).
    """
    template_name = 'wallet-details-view.html'
    model = Wallet
    context_object_name = 'wallet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = Expense.objects.filter(wallet=self.get_object())
        context['total_amount'] = sum([e.amount for e in context['expenses']])
        context['total_expenses'] = len(context['expenses'])
        return context


class CreateExpenseView(IsAccountOwner, FormView):
    """
    Add new expense to wallet view.
    Restricted to account owners (logged in user must be account owner).
    """
    template_name = 'create-expense-view.html'
    form_class = CreateExpenseForm

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Create new expense when form is valid
        """
        expense = Expense(
            wallet=Wallet.objects.get(pk=self.kwargs['wallet_pk']),
            category=form.cleaned_data['category'],
            name=form.cleaned_data['name'],
            amount=form.cleaned_data['amount'],
            description=form.cleaned_data['description'],
            pin=form.cleaned_data['pin']
        )
        expense.save()
        expense.tags.set(form.cleaned_data['tags'])
        self.success_url = expense.wallet.get_absolute_url()
        return super().form_valid(form)


class DeleteExpenseView(IsAccountOwner, FormView):
    """
    Delete expense view.
    Restricted to account owners (logged in user must be account owner).
    """
    template_name = 'delete-expense-view.html'
    form_class = DeleteExpenseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense'] = Expense.objects.get(pk=self.kwargs['expense_pk'])
        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """
        Delete expense when form is valid
        """
        expense = Expense.objects.get(pk=form.cleaned_data['expense_pk'])
        self.success_url = expense.wallet.get_absolute_url()
        expense.delete()
        return super().form_valid(form)
