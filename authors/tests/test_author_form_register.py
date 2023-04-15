from unittest import TestCase, skip  # it's a raw test without things of django (Light)

import pytest
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


@pytest.mark.views
@pytest.mark.fast
class AuthorsRegisterFormUnitTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    @parameterized.expand([
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Seu Nome'),
        ('email', 'Seu e-mail'),
        ('password', 'Sua senha'),
        ('password2', 'Repetir a senha'),
    ])
    def test_author_if_placeholder_is_correct(self, field, must_be):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']  # form['first_name'] is a field to get attrs
        self.assertEqual(must_be, placeholder)

    @parameterized.expand([

        ('username', ''),
        ('email', 'Ex: mail@mail.com'),
        ('password', (
                'A senha deve conter caracters especiais, letra maiuscula e minuscula com numeros, com pelo menos 8 '
                'caracters'
        )),

    ])
    def test_author_if_help_messages_is_correct(self, field, must_be):
        form = RegisterForm()
        placeholder = form[field].help_text  # form['first_name'] is a field
        #                                               to get help_text field
        self.assertEqual(must_be, placeholder)

    @parameterized.expand([
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
    ])
    def test_author_if_labels_name_is_correct(self, field, must_be):
        form = RegisterForm()
        placeholder = form[field].label  # form['first_name'] is a field
        #                                                                   to get attrs we user all way
        self.assertEqual(must_be, placeholder)


@pytest.mark.views
class AuthorRegisterFormIntegrationTest(DjangoTestCase):

    def setUp(self) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@valid.com.br',
            'password': 'Str0ng@123',
            'password2': 'Str0ng@123',
        }
        return super(AuthorRegisterFormIntegrationTest, self).setUp()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
        ('password', 'A senha não pode ser vazia'),
        ('password2', 'A senha não pode ser vazia'),

    ])
    def test_fields_cannot_be_empty(self, field, alert_msg):
        self.form_data[field] = " "
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)  # Follow means will redirect when in needed
        # self.assertIn(alert_msg, response.content.decode('utf-8')) # return all site in html to compare (content)
        self.assertIn(alert_msg, response.context['form'].errors.get(field))  # has more precision than content (this
        #                                        return just what he found about the field inside of form (context)

    @parameterized.expand([
        ('first_name', 'Certifique-se de que o valor tenha no máximo 150 caracteres (ele possui 152).'),
        ('last_name', 'Certifique-se de que o valor tenha no máximo 150 caracteres (ele possui 152).'),
        ('username', 'Certifique-se de que o valor tenha no máximo 150 caracteres (ele possui 152).'),
        ('password', 'Certifique-se de que o valor tenha no máximo 128 caracteres (ele possui 152).'),
    ])
    def test_field_max_length(self, field, value):
        url = reverse('authors:register_create')
        self.form_data[field] = ('1' * 50) + '@' + ('A' * 50) + '.' + ('a' * 50)
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(value, response.context['form'].errors.get(field))

    @parameterized.expand([
        ('first_name', 'Certifique-se de que o valor tenha no mínimo 4 caracteres (ele possui 2).'),
        ('last_name', 'Certifique-se de que o valor tenha no mínimo 4 caracteres (ele possui 2).'),
    ])
    def test_field_min_length(self, field, value):
        url = reverse('authors:register_create')
        self.form_data[field] = 'ab'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(value, response.context['form'].errors.get(field))

    def test_field_password_has_Upper_Lower_case_and_numbers(self):
        value = 'A senha deve conter caracters especiais, letra maiuscula e minuscula com numeros, com pelo menos 8 ' \
                'caracters'  # noqa
        url = reverse('authors:register_create')
        self.form_data['password'] = 'abc'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(value, response.content.decode('utf-8'))

    def test_field_password_match_in_both_fields(self):  # try diferents pass in order to return a error
        error_value = 'As senhas são divergentes'
        url = reverse('authors:register_create')
        self.form_data['password'] = '123@Mudar'
        self.form_data['password2'] = '123@Mudarr'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(error_value, response.content.decode('utf-8'))

    @parameterized.expand([
        ('first_name', 'root', 'Nome já esta em uso: root'),
        ('first_name', '#AnyName', 'Somente letras e numeros são permitidos'),
        ('first_name', 'two names', 'Somente o primeiro nome nesse campo'),
        ('username', 'two names', 'Informe um nome de usuário válido. Este valor pode conter apenas letras, números e '
                                  'os seguintes caracteres @/./+/-/_.'),
    ])
    def test_field_cases_of_names_fields_if_they_accept_properly(self, field, arg_case, error_expect):
        url = reverse('authors:register_create')
        self.form_data[field] = arg_case
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(error_expect, response.content.decode('utf-8'))
        self.assertRedirects(response, reverse('authors:register'))

    def test_if_every_works_properly_with_corrects_parameters(self):
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Usuario Cadastrado com Sucesso!!!"
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertRedirects(response, reverse('farmacia:home'))

    def test_if_get_error_404_if_not_post(self):
        response = self.client.get(reverse('authors:register_create'))
        self.assertEqual(response.status_code, 404)

    def test_if_exists_email(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = "Email já em uso"
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_user_can_login_with_a_register_created_account(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'usertest',
            'password': '123@Mudar',
            'password2': '123@Mudar',
        })
        self.client.post(url, data=self.form_data, follow=True)
        bool_login = self.client.login(username='usertest', password='123@Mudar')
        self.assertTrue(bool_login)

    def test_if_form_is_not_valid_redirect_to_register(self):
        response = self.client.post(reverse('authors:register_create'), data={'username': 'invalid'}, follow=True)
        self.assertRedirects(response, reverse('authors:register'))
        self.assertNotIn('Falha ao criar o usuario', response.content.decode('utf-8'))

    @skip("ainda não sei como fazer")
    def test_invalid_form_user_data_returns_msg_error(self):
        self.form_data.update({
            'first_name': ('@' * 200),
        })
        response = self.client.post(reverse('authors:register_create'), data=self.form_data, follow=True)
        self.assertIn('Falha ao criar o usuario', response.content.decode('utf-8'))
        self.assertRedirects(response, reverse('authors:register'))
