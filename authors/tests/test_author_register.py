from unittest import TestCase  # it's a raw test without things of django (Light)
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm, name_validator


class AuthorsRegisterFormUnitTest(TestCase):
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
                '''A senha deve conter caracters especiais, letra maiuscula e minuscula com numeros,
            com pelo menos 8 caracters'''
        )),

    ])
    def test_author_if_help_messages_is_correct(self, field, must_be):
        form = RegisterForm()
        placeholder = form[field].help_text  # form['first_name'] is a field
        #                                               to get help_text field
        self.assertEqual(must_be, placeholder)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
    ])
    def test_author_if_labels_name_is_correct(self, field, must_be):
        form = RegisterForm()
        placeholder = form[field].label  # form['first_name'] is a field
        #                                                                   to get attrs we user all way
        self.assertEqual(must_be, placeholder)


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

    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
        ('password', 'A senha não pode ser vazia'),
        ('password2', 'A senha não pode ser vazia'),

    ])
    def test_fields_cannot_be_empty(self, field, alert_msg):
        self.form_data[field] = " "
        url = reverse('authors:create')
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
        url = reverse('authors:create')
        self.form_data[field] = ('1' * 50) + '@' + ('A' * 50) + '.' + ('a' * 50)
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(value, response.context['form'].errors.get(field))

    @parameterized.expand([
        ('first_name', 'Certifique-se de que o valor tenha no mínimo 4 caracteres (ele possui 2).'),
        ('last_name', 'Certifique-se de que o valor tenha no mínimo 4 caracteres (ele possui 2).'),
    ])
    def test_field_min_length(self, field, value):
        url = reverse('authors:create')
        self.form_data[field] = 'ab'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(value, response.context['form'].errors.get(field))

    def test_field_password_has_Upper_Lower_case_and_numbers(self):
        value = 'A senha é invalida, deve conter letras maiusculas e minusculas alem de numeros'
        url = reverse('authors:create')
        # self.form_data[field] = 'ab'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(value, response.content.decode('utf-8'))

    def test_field_password_match_in_both_fields(self):
        error_value = 'A senha é invalida, deve conter letras maiusculas e minusculas alem de numeros'
        url = reverse('authors:create')
        # self.form_data[field] = 'ab'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(error_value, response.content.decode('utf-8'))
