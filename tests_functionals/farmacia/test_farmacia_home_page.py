import os
from unittest.mock import patch

import pytest
from .base_Funcitional_Test import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

METHOD_MODE = os.environ.get('METHOD_MODE')

@pytest.mark.functional_test
class TestFunctionalHomePage(BaseTest):

    def test_If_No_Medicines_Home_Page(self):
        self.browser.get(self.live_server_url)

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Sem Estoque', body.text)

    def test_If_Has_Medicine_Home_Page(self):
        self.make_medicine_no_defaults(10)
        self.browser.get(self.live_server_url)

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertNotIn("Sem Estoque", body.text)

    def test_Search_Find_Properly(self):
        # open window, click in search input, digit term and click in search button
        medicine = self.make_medicine_no_defaults(5)
        term = medicine[0].title  # get title in order to research
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Digite aqui sua busca"]'
        )
        search_input.send_keys(term)
        search_input.send_keys(Keys.ENTER)
        self.assertIn(term, self.browser.find_element(By.TAG_NAME, 'body').text)

    if METHOD_MODE == '1':
        @patch('farmacia.views.func_views.OBJ_PER_PAGE', new=3)
        def test_Pagination_Home_if_Page_2_is_has_3_elements(self):
            # make medicines data:
            self.make_medicine_no_defaults(10)
            # open the page:
            self.browser.get(self.live_server_url)
            # see that has a page 2 option and click there
            # page_move = self.browser.find_element(By.XPATH, '//a[@aria-role="page 2"]')
            page_move = self.browser.find_element(By.XPATH, '/html/body/nav/form/a[2]')
            page_move.click()
            self.sleep(4)
    else:
        @patch('farmacia.views.class_views.OBJ_PER_PAGE', new=3)
        def test_Pagination_Home_if_Page_2_is_has_3_elements(self):
            # make medicines data:
            self.make_medicine_no_defaults(10)
            # open the page:
            self.browser.get(self.live_server_url)
            # see that has a page 2 option and click there
            # page_move = self.browser.find_element(By.XPATH, '//a[@aria-role="page 2"]')
            page_move = self.browser.find_element(By.XPATH, '/html/body/nav/form/a[2]')
            page_move.click()
            self.sleep(4)

            self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'object-view')), 3)
