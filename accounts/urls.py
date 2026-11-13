from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),  # POST only
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/owner/", views.owner_dashboard, name="owner_dashboard"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
]
