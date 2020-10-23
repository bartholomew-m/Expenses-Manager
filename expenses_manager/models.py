from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """
    Account model.
    User can have many accounts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)

    @property
    def wallet_count(self) -> int:
        """
        How many wallets are attached do an account.
        """
        return Wallet.objects.filter(account=self).count()

    class Meta:
        ordering = ('user', 'name')

    def __str__(self) -> str:
        return f'Account(user: {self.user.username}, name: {self.name})'


class Tag(models.Model):
    """
    Tag model.
    Wallets can have tags, and expenses can have tags.
    Managable from admin panel.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Wallet(models.Model):
    """
    Wallet model.
    Wallet is attached to account.
    Account can have many wallets.
    """
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    @property
    def absolute_url(self) -> str:
        """
        Get url for templates as a property
        """
        return self.get_absolute_url()

    def get_absolute_url(self) -> str:
        """
        Get url for views
        """
        return f'/expenses-manager/accounts/{self.account.pk}/wallets/{self.pk}/'

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return f'Wallet(name: {self.name}, account: {self.account})'


class ExpenseCategory(models.Model):
    """
    Expense category.
    Managable from admin panel.
    """
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return f'ExpenseCategory(name: {self.name})'


class Expense(models.Model):
    """
    Expense model.
    Expense is attached to a wallet.
    Wallet can have many expenses.
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=500, blank=True, null=True)
    pin = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('wallet', '-pin', '-created',)

    def __str__(self) -> str:
        return f'Expense(pinned: {self.pin}, name: {self.name}, amount: {self.amount}, description: {self.description}, wallet: {self.wallet})'
