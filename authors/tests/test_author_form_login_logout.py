from unittest import skip

import pytest
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse


@pytest.mark.fast
class AuthorTest(TestCase):
    def test_author_if_method_not_post(self):
        response = self.client.get(reverse('authors:authenticate'))
        self.assertEqual(response.status_code, 404)

    def test_logout_if_redirect(self):
        User.objects.create_user(username='user', password='true')
        self.client.login(username='user', password='true')
        response = self.client.post(reverse('authors:logout'),follow=True)
        self.assertRedirects(response, reverse('farmacia:home'))

    def test_logout_if_method_not_post(self):
        User.objects.create_user(username='user', password='true')
        self.client.login(username='user', password='true')
        response = self.client.get(reverse('authors:logout'))
        self.assertEqual(response.status_code, 404)