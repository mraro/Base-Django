from unittest import skip

import pytest
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse


@pytest.mark.views
@pytest.mark.fast
class AuthorTest(TestCase):
    def test_author_if_method_not_post(self):
        response = self.client.get(reverse('authors:authenticate'))
        self.assertGreater(response.status_code, 403)

    def test_logout_if_redirect(self):
        User.objects.create_user(username='user', password='true')
        self.client.login(username='user', password='true')
        response = self.client.post(reverse('authors:logout'), data={'username': 'user'}, follow=True)
        self.assertRedirects(response, reverse('farmacia:home'))

    def test_logout_if_has_first_name(self):
        User.objects.create_user(username='user', first_name='first', password='true')
        self.client.login(username='user', password='true')
        response = self.client.post(reverse('authors:logout'), data={'username': 'user', 'first_name': 'first'},
                                    follow=True)
        self.assertIn('Até mais first', response.content.decode('utf-8'))

    def test_logout_if_method_not_post(self):
        User.objects.create_user(username='user', password='true')
        self.client.login(username='user', password='true')
        response = self.client.get(reverse('authors:logout'))
        self.assertGreaterEqual(response.status_code, 404)

    def test_user_tries_logout_another_user(self):
        User.objects.create_user(username='user', password='true')
        self.client.login(username='user', password='true')
        response = self.client.post(reverse('authors:logout'), data={'username': 'otheruser'}, follow=True)
        self.assertRedirects(response, reverse('authors:login'))

    def test_login_authenticate_form_invalid(self):
        response = self.client.post(reverse('authors:authenticate'), data={'username': '  ', 'password': '  '},
                                    follow=True)
        self.assertRedirects(response, reverse('authors:login'))
        self.assertIn('preencha os campos corretamente', response.content.decode('utf-8'))
