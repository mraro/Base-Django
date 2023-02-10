from unittest import skip

from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse

@skip
class AuthorTest(TestCase):
    def test_author_invalid_credentials(self):
        User.objects.create_user(username='user', password='true')
        response = self.client.get(reverse('authors:login'), follow=True)
        self.client.login(username=' ', password=' ')

        url = reverse('authors:logout')
        response = self.client.post(url, follow=True)
        msg = "preencha os campos corretamente"
        self.assertIn(msg, response.content.decode('utf-8'))
