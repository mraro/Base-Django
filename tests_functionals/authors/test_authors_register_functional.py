from parameterized import parameterized

from .base_Functional_Test_Authors import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsRegisterTest(AuthorsBaseTest):
    @parameterized.expand([
        ("Primeiro nome",   '     ',  'Este campo é obrigatório.'),
        ("Sobrenome",       '     ',  'Este campo é obrigatório.'),
        ("Seu Nome",        '     ',  'Este campo é obrigatório.'),
        # ("Seu e-mail",      '     ',  'Informe um endereço de email válido.'),
        ("Sua senha",       '     ', 'A senha não pode ser vazia'),
        ("Repetir a senha", '     ', 'A senha não pode ser vazia'),
    ])
    def test_form_fields_errors_in_register(self, field, value, asserted):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(By.XPATH, '/html/body/form')
        self.fill_fields_to_testing(form)
        field = self.get_by_placeholder(form, field)
        field.send_keys(value)
        field.send_keys(Keys.ENTER)
        form = self.browser.find_element(By.XPATH, '/html/body/form')

        self.assertIn(asserted, form.text)

    def test_form_field_password_is_the_same(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(By.XPATH, '/html/body/form')
        self.fill_fields_to_testing(form)
        self.get_by_placeholder(form, 'Sua senha').send_keys('123@Mudar')
        self.get_by_placeholder(form, 'Repetir a senha').send_keys('123@MudarDifernte')
        self.browser.find_element(By.XPATH, '/html/body/form/button').click()

        form = self.browser.find_element(By.XPATH, '/html/body/form')

        self.assertIn('As senhas são divergentes', form.text)

    def test_form_is_able_to_registrate(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(By.XPATH, '/html/body/form')
        self.get_by_placeholder(form, 'Primeiro nome').send_keys('Usuario')
        self.get_by_placeholder(form, 'Sobrenome').send_keys('Teste')
        self.get_by_placeholder(form, 'Seu Nome').send_keys('tester')
        self.get_by_placeholder(form, 'Seu e-mail').send_keys('email@email.valid')
        self.get_by_placeholder(form, 'Sua senha').send_keys('123@Mudar')
        self.get_by_placeholder(form, 'Repetir a senha').send_keys('123@Mudar')
        self.browser.find_element(By.XPATH, '/html/body/form/button').click()

        form = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn("Usuario Cadastrado com Sucesso!!!", form.text)
