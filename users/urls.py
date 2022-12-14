from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("profile/", views.EditProfileView.as_view(), name="profile"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="signing"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("remove_account/", views.RemoveAccountView.as_view(), name="remove_account"),
    path("my/", views.MyItemView.as_view(), name="my_items"),
    path('reset_password/', views.MyPasswordResetView.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('email/verify', views.EmailVerify.as_view(), name='email_verify'),
]
