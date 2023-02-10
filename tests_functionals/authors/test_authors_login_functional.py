import time
from unittest import skip

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base_Functional_Test_Authors import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_if_is_able_to_Login(self):
        # we create a fake user to test:
        user = User.objects.create_user(username="TOLO", password="Tolete@123")
        user.save()
        # access the page of login and find form:
        self.browser.get(self.live_server_url + reverse('authors:login'))
        body = self.browser.find_element(By.TAG_NAME, 'body')
        # will add login credentials
        self.get_by_placeholder(body, 'Digite seu usuario').send_keys("TOLO")
        self.get_by_placeholder(body, 'Digite sua senha').send_keys("Tolete@123")
        # time.sleep(3)
        body.find_element(By.XPATH, '/html/body/div/form/div[3]/button').click()
        # time.sleep(3)

        self.assertIn("Sucesso no Login!", self.browser.find_element(By.XPATH, '/html/body/div[1]').text)

    def test_login_create_raises_404_if_not_POST(self):
        self.browser.get(self.live_server_url + reverse('authors:create'))
        self.assertIn('Not Found', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_authenticate_if_is_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.get_by_placeholder(body, 'Digite seu usuario').send_keys("False")
        self.get_by_placeholder(body, 'Digite sua senha').send_keys("Fail")
        body.find_element(By.XPATH, '/html/body/div/form/div[3]/button').click()
        time.sleep(3)
        body = self.browser.find_element(By.TAG_NAME, 'body')  # has this because has a redirect to same page

        self.assertIn('Usuario e/ou senha incorretos', body.text)

