from expenses_manager.models import Account
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser


def _get_account_pk(url_path: str) -> int:
    """
    Extract url account id as int
    """
    start = url_path.find('accounts/') + 9
    end = url_path.find('/', start)
    return int(url_path[start:end])


class IsLoggedIn(PermissionRequiredMixin):
    """
    Check if request.user is logged in (not Anonymous user)
    """
    def has_permission(self) -> bool:
        return self.request.user.is_authenticated


class IsAccountOwner(IsLoggedIn):
    """
    Check if user is logged in and request.user is account.user (owner of the account)
    """
    def has_permission(self) -> bool:
        try:
            account_pk = _get_account_pk(self.request.path)
            if type(self.request.user) == AnonymousUser:
                return False
            account: Account = Account.objects.get(pk=account_pk)
            return super().has_permission() and account.user == self.request.user
        except ValueError:
            raise ValueError('IsAccountOwner permission -> no account_pk in url')
