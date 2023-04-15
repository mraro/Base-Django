import os
from unittest.mock import patch

import pytest
from django.urls import reverse
from parameterized import parameterized
from rest_framework import test
from farmacia.tests.tests_medicine_base import BaseMixing
import dotenv
dotenv.load_dotenv()

env_var_method_used = os.environ.get("METHOD_MODE")


def method_used(boolean):
    if boolean == '0':
        return 'farmacia.views.api_views.api_djangorest_class.OurPagination.page_size'
    elif boolean == '1':
        return 'farmacia.views.api_views.api_djangorest.OBJ_PER_PAGE'
    else:
        raise ValueError


@pytest.mark.apiTest
class MedicineTestApiV2Class(test.APITestCase, BaseMixing):

    def response(self, reverse_path, **kwargs):
        if kwargs:
            first = next(iter(kwargs.values()))
        else:
            first = None
        return self.client.get(reverse(reverse_path, kwargs=first))

    def test_home_response_apiV2_status_200(self):
        response = self.response('farmacia:home_rest')
        self.assertIs(response.status_code, 200)

    @patch(method_used(env_var_method_used), new=7)
    def test_home_how_many_objects_loads_in_a_single_page(self):
        self.make_medicine_no_defaults(18)
        num_of_medicines = 7
        response = self.response('farmacia:home_rest')
        qtd_medicines_has_loaded = len(response.data['results'])
        self.assertEqual(num_of_medicines, qtd_medicines_has_loaded)

    @patch(method_used(env_var_method_used), new=7)
    def test_home_pagination_works_properly(self):
        self.make_medicine_no_defaults(19)

        response = self.client.get(reverse('farmacia:home_rest') + '?page=2')
        self.assertEqual(len(response.data.get('results')), 7)

    @patch(method_used(env_var_method_used), new=87)
    def test_home_if_shows_unpublished_objects_in_production(self):
        medicines = self.make_medicine_no_defaults(2)
        medicine_published = medicines[0]
        medicine_published.is_published = True
        medicine_published.title = "PUBLISHED"
        medicine_published.full_clean()
        medicine_published.save()
        medicine_not_published = medicines[1]
        medicine_not_published.is_published = False
        medicine_not_published.title = "NOT PUBLISHED"
        medicine_not_published.full_clean()
        medicine_not_published.save()
        response = self.response('farmacia:home_rest')
        self.assertIn("PUBLISHED", response.content.decode('utf-8'))
        self.assertNotIn("NOT PUBLISHED", response.content.decode('utf-8'))

    def test_detail_page_is_just_one_object_and_is_properly_object(self):
        medicines = self.make_medicine_no_defaults(2)
        pk = medicines[0].id
        response = self.response("farmacia:remedio_rest", kwargs={'pk': pk})
        self.assertIn(medicines[0].title, response.content.decode('utf-8'))

    @patch(method_used(env_var_method_used), new=10)
    def test_category_lists_properly_if_requested(self):
        category_searched = self.make_category('CATEGORY TO SHOW')
        category_not_be_showed = self.make_category('CATEGORY TO NOT SHOW')
        medicines = self.make_medicine_no_defaults(8)
        for medicine in medicines:
            medicine.category = category_searched
            medicine.save()

        medicines[0].category = category_not_be_showed
        medicines[0].save()  # here it made a blacking ship that shouldn't be showed and then for this reason less 1
        # on assertEqual

        response = self.response('farmacia:categoria_rest', kwargs={'idcategoria': category_searched.id})
        # get category by id ^^

        self.assertIn('CATEGORY TO SHOW', response.content.decode('utf-8'))  # to make sure that has this category
        self.assertEqual(len(response.data['results']), len(medicines) - 1)  # was definided len(medicines) - 1 because
        # make_medicine_no_default may create less than is solicited, since he suprime errors

    @parameterized.expand(['THIS_title',
                           'THIS_category',
                           'THIS_description', ])
    def test_search_returns_properly_searching_for_parameterized(self, search):
        medicine0 = self.make_medicines(title="THIS_title", slug='1', author_data={
            'username': "Joaozinho1"
        })
        medicine1 = self.make_medicines(category="THIS_category", slug='2', author_data={
            'username': "Joaozinho2"
        })
        medicine2 = self.make_medicines(description="THIS_description", slug='3', author_data={
            'username': "Joaozinho3"
        })

        medicine0.save()
        medicine1.save()
        medicine2.save()
        response = self.client.get(reverse('farmacia:search_rest') + f'?q={search}')

        self.assertEqual(len(response.data['results']), 1)

    def test_search_without_value_returns_404(self):
        response = self.client.get(reverse('farmacia:search_rest'))
        self.assertEqual(response.status_code, 404)

    def test_tag_list_all_values_that_refers_a_tag(self):
        medicines = self.make_medicine_no_defaults(5)
        tag = self.make_tags("TAG Name")
        for medicine in medicines:
            medicine.tags.add(tag)
            medicine.save()

        response = self.response('farmacia:tag_rest', kwargs={'slug': tag.slug})
        self.assertEqual(len(response.data['results']), 5)


