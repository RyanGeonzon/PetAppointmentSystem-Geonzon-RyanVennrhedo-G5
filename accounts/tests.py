from django.test import TestCase
from django.urls import reverse
from .models import User


class AccountTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("own", "own@x.com", "Passw0rd!xyz")
        self.admin = User.objects.create_superuser("adm", "adm@x.com", "Passw0rd!xyz")

    def test_register_hashes_password_and_rejects_duplicate_email(self):
        data = {"username": "new", "first_name": "A", "last_name": "B", "email": "new@x.com",
                "password1": "Str0ng!Pass99", "password2": "Str0ng!Pass99"}
        self.client.post(reverse("accounts:register"), data)
        u = User.objects.get(username="new")
        self.assertNotEqual(u.password, "Str0ng!Pass99"); self.assertEqual(u.role, "owner")
        data["username"] = "other"; data["email"] = "NEW@x.com"
        r = self.client.post(reverse("accounts:register"), data)
        self.assertFalse(User.objects.filter(username="other").exists())

    def test_password_mismatch(self):
        r = self.client.post(reverse("accounts:register"), {"username": "z", "first_name": "a", "last_name": "b",
            "email": "z@x.com", "password1": "Str0ng!Pass99", "password2": "different"})
        self.assertFalse(User.objects.filter(username="z").exists())

    def test_login_required_redirect(self):
        r = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(r, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")

    def test_invalid_login(self):
        r = self.client.post(reverse("accounts:login"), {"username": "own", "password": "bad"})
        self.assertContains(r, "Invalid username or password")

    def test_role_redirect_and_isolation(self):
        self.client.login(username="own", password="Passw0rd!xyz")
        self.assertRedirects(self.client.get("/"), reverse("accounts:owner_dashboard"))
        self.assertEqual(self.client.get(reverse("accounts:admin_dashboard")).status_code, 403)
        self.client.logout(); self.client.login(username="adm", password="Passw0rd!xyz")
        self.assertRedirects(self.client.get("/"), reverse("accounts:admin_dashboard"))
        self.assertEqual(self.client.get(reverse("accounts:owner_dashboard")).status_code, 403)

    def test_profile_update_and_logout(self):
        self.client.login(username="own", password="Passw0rd!xyz")
        self.client.post(reverse("accounts:profile_edit"), {"first_name": "Jo", "last_name": "D", "email": "own@x.com", "phone": "0917"})
        self.owner.refresh_from_db(); self.assertEqual(self.owner.phone, "0917")
        self.client.post(reverse("accounts:logout"))
        self.assertEqual(self.client.get(reverse("accounts:profile")).status_code, 302)
