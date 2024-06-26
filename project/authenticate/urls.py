from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register/<str:role>', views.register, name='register'),
    path('logout', views.logoutAccount, name='logoutAccount'),
    path('unauthorized', views.unauthorized, name='unauthorized'),
    
    # Email verification urls
    path('activate-email-sent', views.activateEmailSent, name='activateEmailSent'),
    path('activate-link-invalid', views.activateLinkInvalid, name='activateLinkInvalid'),
    path('activate/<uidb64>/<token>', views.activateAccount, name='activateAccount'),
    
    # Password Reset urls
    path('reset-password',          auth_views.PasswordResetView.as_view(           template_name='authenticate/password_reset_form.html'   ), name='password_reset'),
    path('reset-password-sent',     auth_views.PasswordResetDoneView.as_view(       template_name='authenticate/password_reset_sent.html'   ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(    template_name='authenticate/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(   template_name='authenticate/password_reset_done.html'   ), name='password_reset_complete'),
    
    # path('registerCustomer', views.registerCustomer, name='registerCustomer')
]