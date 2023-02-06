from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from farmacia.tests.tests_medicine_base import BaseMixing
from utility.browser import make_chrome_browser
import time


class BaseTest(StaticLiveServerTestCase, BaseMixing):
    def setUp(self) -> None:
        self.make_medicine_no_defaults()
        self.browser = make_chrome_browser()
        self.browser.get(self.live_server_url)
        return super().setUp()

    def tearDown(self) -> None:
        self.sleep()
        self.browser.quit()
        return super().tearDown()

    @staticmethod
    def sleep(seconds=3):  # Time that shows windows
        time.sleep(seconds)