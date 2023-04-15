import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from farmacia.tests.tests_medicine_base import BaseMixing


# ## Base model to test authenticated:
class MethodBaseWithAuthToTestAPIv2(APITestCase):
    def authenticate_api(self, num_user_choice):    # two users to create and authenticate, can be more
        users = [["Json01", "123@Mudar"], ["Json02", "123@Mudar"]]

        for user in users:
            User.objects.create_user(username=user[0], password=user[1])
        # this is a way to pretend to send a json file:
        form = {
            "username": users[num_user_choice][0],
            "password": users[num_user_choice][1],
        }
        response = self.client.post(reverse('authors:token_obtain_pair'), data=form)
        return response

    def create_an_object(self, title, access_token):
        """ create a raw object in order to test """
        form = {

            "id": 361,
            "title": title,
            "price": "12.00",
            "quantity": 0,
            "description": "descript",
        }

        response = self.client.post(reverse("authors:rest_create"), data=form,
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        # return this to session test
        return response


# ###### Tests:
@pytest.mark.apiTest
class ManagerUserAPIv2(MethodBaseWithAuthToTestAPIv2):

    def test_if_can_create_user_by_api_request(self):
        form = {
            "first_name": "Jsosn24",
            "last_name": "JsonUsser",
            "username": "supors2teJs4on",
            "email": "JsonUss42er@hmail.com",
            "password": "123@Mudar",
            "password2": "123@Mudar"
        }
        response = self.client.post(reverse('authors:rest_register_create'), data=form, follow=True)
        self.assertEqual(response.status_code, 201)

    def test_auth_create_and_return_tokens_to_api(self):
        response = self.authenticate_api(0)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.content.decode('utf-8'))


@pytest.mark.apiTest
class DashboardCRUD_APIv2(MethodBaseWithAuthToTestAPIv2, BaseMixing):
    def setUp(self) -> None:
        self.response = self.authenticate_api(1)
        self.access_token = self.response.data['access']

        return super().setUp()

    def test_api_v2_create_medicine(self):
        response = self.create_an_object("TITULO 1", self.access_token)
        self.assertEqual(response.status_code, 201)

    def test_api_v2_update_medicine(self):
        # create an object to update after:
        id_needed = self.create_an_object("TITULO 2", self.access_token).data['id']
        # data update:
        form = {
            "title": "TITLE EDITED",
        }
        response = self.client.patch(reverse("authors:rest_edit", kwargs={'pk': id_needed}), data=form,
                                     HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

    def test_api_v2_read_medicine(self):
        # create an object to read:
        self.create_an_object("TITULO to READ", self.access_token)
        self.make_medicine_no_defaults(2)
        # test if page open ok
        response = self.client.get(reverse("authors:rest_dashboard"), HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, 200)  # check if is ok on request
        self.assertEqual(len(response.data), 1)  # check if return just one object created by user

    def test_api_v2_delete_medicine(self):
        id_to_delete = self.create_an_object("TITULO to READ", self.access_token).data['id']
        other = self.make_medicine_no_defaults(1)[0]

        response = self.client.delete(reverse("authors:rest_delete", kwargs={'pk': id_to_delete}),
                                      HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 204)

    def test_api_v2_delete_medicine_that_is_not_own(self):
        other = self.make_medicine_no_defaults(1)[0]  # made an object with a different user

        response = self.client.delete(reverse("authors:rest_delete", kwargs={'pk': other.id}),
                                      HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 404)
