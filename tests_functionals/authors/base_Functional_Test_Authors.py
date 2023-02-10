from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from utility.browser import make_chrome_browser


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
        return web_element.find_element(By.XPATH, '//input[@placeholder="'+placeholder+'"]')

    @staticmethod
    def fill_fields_to_testing(form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys("       ")
        form.find_element(By.NAME, 'email').send_keys('aaa@aaa')