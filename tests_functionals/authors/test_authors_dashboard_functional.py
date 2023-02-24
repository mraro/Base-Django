from django.urls import reverse
from time import sleep

from .base_Functional_Test_Authors import AuthorsBaseTestDashboard, By


class DashboardFunctionalTest(AuthorsBaseTestDashboard):

    def test_functional_create_obj_and_save(self):
        """ THIS TEST SLUG IF TITLE HAS EXISTED AND SLUG HAS EXISTED TOO, HE TEST IF CANS MAKE ANOTHER SLUG """
        self.browser.get(self.live_server_url + reverse('authors:create'))
        self.easy_edit_element_by_name_field('title', self.obj.title)
        self.easy_edit_element_by_name_field('price', self.fake_data['price'])
        self.easy_edit_element_by_name_field('quantity', self.fake_data['quantity'])
        self.easy_edit_element_by_name_field('description', self.fake_data['description'])
        self.browser.find_element(By.ID, 'button-form').click()
        # sleep(5)
        self.assertIn('Remedio criado e enviado a analise', self.browser.find_element(By.TAG_NAME, 'body').text)




    def test_functional_edit_obj_and_save(self):
        self.browser.get(self.live_server_url + reverse('authors:edit', kwargs={'idobject': self.obj.id}))
        self.browser.find_element(By.TAG_NAME, 'body')
        self.easy_edit_element_by_name_field('title', self.fake_data['title'])
        self.browser.find_element(By.XPATH, '/html/body/div/form/button').click()
        sleep(5)
        self.assertIn('Remedio Salvo', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_functional_delete_obj(self):
        self.browser.get(self.live_server_url + reverse('authors:dashboard'))
        self.browser.find_element(By.ID, 'button-delete').click()
        alert_obj = self.browser.switch_to.alert
        alert_obj.accept()
        self.assertIn(f"{self.obj.title} deletado!", self.browser.find_element(By.TAG_NAME, 'body').text)
