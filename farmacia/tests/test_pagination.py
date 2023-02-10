from unittest.mock import patch

from django.test import RequestFactory
from django.urls import reverse

from farmacia.tests.tests_medicine_base import BaseTestMedicine
from utility.paginator import make_paginations


# @skip
class Paginationtest(BaseTestMedicine):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass
    def test_make_pagination_range_return_pagination_range(self):
        request_factory = RequestFactory()
        request = request_factory.get('home', data={'q': 'a'})
        # print(request)
        pagination = make_paginations(request,
                                      obj=list(range(1, 121)),
                                      qty_options=4,
                                      )['pagination']

        self.assertEqual(range(1, 5), pagination)

    def test_make_pagination_range_grader_than_limit_return_pagination_range(self):
        request_factory = RequestFactory()
        request = request_factory.get('home', data={'page': 'a'})
        # print(request)
        pagination = make_paginations(request,
                                      obj=list(range(1, 121)),
                                      qty_options=4,
                                      )['pagination']

        self.assertEqual(range(1, 5), pagination)

    def test_len_max_of_shows_in_pagination_if_is_less_than_middle(self):
        # Current page:3  - Qty pages: 4  - Middle pages: 3
        request_factory = RequestFactory()
        request = request_factory.get('home', data={'page': '24'})
        pagination = make_paginations(request, obj=list(range(1, 160)), qty_options=6)
        # print(pagination['last_range']," / / ",pagination['middle_range']," / / ", request)
        self.assertLessEqual(pagination['current_page'], pagination['last_range'])

    def test_make_pagination_range_test_if_is_not_int_requested(self):
        for i in range(12):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_medicines(**kwargs)

        with patch('farmacia.views.RANGE_PER_PAGE', new=3):  # teoricamente era para sobreescrever a variavel RANGE_PE..
            response = self.client.get(reverse('farmacia:home') + '?page=1A')

            self.assertIn('<a aria-role="page 1" class="pagination-options" name="page" href="?q=&page=1">1</a>',
                          response.content.decode('utf-8'))
