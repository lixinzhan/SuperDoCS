"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from protocols.TG61.tests import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class LogoutPageTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser(
            username='logout-test-user',
            email='logout-test@example.com',
            password='test-password',
        )
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.user)

    def assert_logout_form(self, response):
        self.assertContains(response, 'method="post"')
        self.assertContains(response, 'action="/logout/"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, '<button type="submit"')
        self.assertIn('csrftoken', self.client.cookies)
        return self.client.cookies['csrftoken'].value

    def test_get_does_not_log_out(self):
        response = self.client.get(reverse('logout_page'))

        self.assertEqual(response.status_code, 405)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_post_without_csrf_does_not_log_out(self):
        response = self.client.post(reverse('logout_page'))

        self.assertEqual(response.status_code, 403)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_application_logout_form_logs_out(self):
        page = self.client.get('/help/')
        csrf_token = self.assert_logout_form(page)

        response = self.client.post(
            reverse('logout_page'),
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertRedirects(response, '/')
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_admin_logout_form_logs_out(self):
        page = self.client.get(reverse('admin:index'))
        csrf_token = self.assert_logout_form(page)

        response = self.client.post(
            reverse('logout_page'),
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertRedirects(response, '/')
        self.assertNotIn(SESSION_KEY, self.client.session)

