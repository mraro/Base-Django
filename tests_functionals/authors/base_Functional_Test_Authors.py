from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

from utility.browser import make_chrome_browser
from farmacia.tests.tests_medicine_base import BaseMixing


class AuthorsBaseTestDashboard(StaticLiveServerTestCase, BaseMixing):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        self.fake_data = {'title': 'NEW_DATA', 'price': '30.30', 'quantity': '30', 'description': 'DESCRIPT'}

        user = User.objects.create_user(username='username', password='true')
        user.save()
        # access the page of login and find form:
        self.browser.get(self.live_server_url + reverse('authors:login'))
        body = self.browser.find_element(By.TAG_NAME, 'body')
        # will add login credentials
        body.find_element(By.XPATH, '//input[@placeholder="' + 'Digite seu usuario' + '"]').send_keys("username")
        body.find_element(By.XPATH, '//input[@placeholder="' + 'Digite sua senha' + '"]').send_keys("true")
        # time.sleep(3)
        body.find_element(By.ID, 'button-form').click()
        self.obj = self.make_medicine_no_defaults(1)[0]  # creates a object to test made in shell
        self.obj.author = user
        self.obj.is_published = False
        self.obj.save()
        return super().setUp()

    def tearDown(self) -> None:
        sleep(2)
        self.browser.quit()
        return super().tearDown()

    def easy_edit_element_by_name_field(self, field_name, new_value):
        return self.browser.find_element(By.NAME, field_name).send_keys(new_value)


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        # sleep(5)
        self.browser.quit()
        return super().tearDown()

    @staticmethod
    def get_by_placeholder(web_element, placeholder):
        return web_element.find_element(By.XPATH, '//input[@placeholder="' + placeholder + '"]')

    @staticmethod
    def fill_fields_to_testing(form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys("       ")
        form.find_element(By.NAME, 'email').send_keys('aaa@aaa')
