from users import views
from django.urls import path

app_name = "users"

urlpatterns = [
    path("profile/", views.EditProfileView.as_view(), name="profile"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="signin"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("remove_account/", views.RemoveAccountView.as_view(), name="remove_account"),
    path("my/", views.MyItemView.as_view(), name="my_items"),
]
