from django.contrib.auth import views
from django.urls import path
from accounts.views import signup
urlpatterns = [
        path('signup/', signup, name="signup"),
        path('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
        path('logout/', views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
        path('password-reset/', views.PasswordResetView.as_view(template_name='registration/reset_form.html'), name='password_reset'),
        path('password-reset/done/', views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
        path('password-change/', views.PasswordChangeView.as_view(template_name='registration/change_form.html'), name='password_change'),
        path('password-change/done/', views.PasswordChangeDoneView.as_view(template_name='registration/change_done.html'), name='password_change_done'),
]