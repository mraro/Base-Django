import pytest
from base_Funcitional_Test import BaseTest
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class TestFunctionalHomePage(BaseTest):
    def testIfNoMedicinesHomePage(self):
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Sem Estoque', body.text)

    def testIfHasMedicineHomePage(self):
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertNotIn("Sem Estoque", body.text)