from unittest import skip

import pytest
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse

from farmacia.tests.tests_medicine_base import BaseMixing


@pytest.mark.fast
@pytest.mark.views
class AuthorDashboardCRUD(TestCase, BaseMixing):
    """ this tests will test pages on dashboard, like create, read, edit and delete """

    def setUp(self):
        # Setup run before every test method.
        usuario = User.objects.create_user(username='username', password='true')
        self.client.login(username='username', password='true')
        self.obj = self.make_medicine_no_defaults(1)[0]
        self.obj.author = usuario
        self.obj.is_published = False
        self.obj.save()

    def tearDown(self):
        # Clean up run after every test method.
        self.client.logout()

    def test_dashboard_view_every_objects_according_with_author(self):
        response = self.client.get(reverse('authors:dashboard'))
        self.assertIn(self.obj.title, response.content.decode('utf-8'))

    def test_dashboard_render_template_properly(self):
        response = self.client.get(reverse('authors:dashboard'))
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    """@skip
    def test_dashboard_edit_obj_can_edit_an_object(self):
         ''' here I can't click on save, will test with selenium '''
        form = {'title': 'NEW', 'price': '30.30', 'quantity': '2', 'description': 'DESCRIPT'}
        response = self.client.post(f'/authors/dashboard/{self.obj.id}/edit/', data=form, follow=True)
        self.assertIn('Remedio Salvo', response.content.decode('utf-8'))"""

    def test_dashboard_delete_return_404_if_not_post(self):
        response = self.client.get(reverse('authors:delete', args=str(self.obj.id)), follow=True)
        self.assertEqual(response.status_code, 404)
