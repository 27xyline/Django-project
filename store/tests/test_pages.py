from django.test import TestCase
from django.urls import reverse


class LoginPageTestCase(TestCase):
    def test_login_page_contains_google_login_form(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Войти через Google")
        self.assertContains(response, reverse("social:begin", args=["google-oauth2"]))
        self.assertContains(response, "csrfmiddlewaretoken")
