from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .decorators import role_required
from .forms import LoginForm, ProfileForm, RegisterForm
from .models import User

ROLE_HOME = {User.Role.ADMIN: "accounts:admin_dashboard", User.Role.OWNER: "accounts:owner_dashboard"}


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect("accounts:login")
        messages.error(request, "Please fix the errors below.")
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


@login_required
def dashboard(request):
    """Sends each user to the dashboard for their role."""
    return redirect(ROLE_HOME.get(request.user.role, "accounts:owner_dashboard"))


@role_required(User.Role.ADMIN)
def admin_dashboard(request):
    ctx = {
        "total_users": User.objects.count(),
        "owner_count": User.objects.filter(role=User.Role.OWNER).count(),
        "recent_users": User.objects.order_by("-date_joined")[:10],
    }
    return render(request, "accounts/admin_dashboard.html", ctx)


@role_required(User.Role.OWNER)
def owner_dashboard(request):
    return render(request, "accounts/owner_dashboard.html")


@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"profile_user": request.user})


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
        messages.error(request, "Please fix the errors below.")
    return render(request, "accounts/profile_edit.html", {"form": form})
