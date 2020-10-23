from django.urls import path
from expenses_manager import views


urlpatterns = [
    path('logout/',
        views.logout_view,
        name='logout'),
    path('login/',
        views.LoginView.as_view(),
        name='login'),
    path('home/',
        views.HomeView.as_view(),
        name='home'),
    path('create-account/',
        views.CreateAccountView.as_view(),
        name='create-account'),
    path('accounts/<int:pk>/',
        views.AccountDetailsView.as_view(),
        name='account-details'),
    path('accounts/<int:account_pk>/create-wallet/',
        views.CreateWalletView.as_view(),
        name='create-wallet'),
    path('accounts/<int:account_pk>/wallets/<int:pk>/',
        views.WalletDetailsView.as_view(),
        name='wallet-details'),
    path('accounts/<int:account_pk>/wallets/<int:wallet_pk>/create-expense/',
        views.CreateExpenseView.as_view(),
        name='create-expense'),
    path('accounts/<int:account_pk>/wallets/<int:wallet_pk>/delete-expense/<int:expense_pk>/',
        views.DeleteExpenseView.as_view(),
        name='delete-expense')
]
