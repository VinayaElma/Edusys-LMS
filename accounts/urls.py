
from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

#app_name= 'accounts'

urlpatterns = [
    path('', accounts_views.home_screen, name="home"),    
    path('login/', accounts_views.loginPage, name="login"),  
    path('register/', accounts_views.RegisterPage.as_view(), name="register"),
    path('changepassword/', accounts_views.change_password, name="changepassword"),
    path('profile/', accounts_views.profilePage, name="profile"),
    path('profile/editprofile/', accounts_views.edit_profile, name="edit_profile"),
    path('logout/', accounts_views.logoutUser, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

