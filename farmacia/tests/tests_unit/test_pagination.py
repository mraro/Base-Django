
from django.test import RequestFactory

from farmacia.tests.tests_medicine_base import BaseTestMedicine
from farmacia.utility.paginator import make_paginations


# @skip
class Paginationtest(BaseTestMedicine):
    def test_make_pagination_range_return_pagination_range(self):
        request_factory = RequestFactory()
        request = request_factory.get('home',data={'q':'a'})
        print(request)
        pagination = make_paginations(request,
                                      obj=list(range(1, 121)),
                                      qty_options=4,
                                      )['pagination']

        self.assertEqual(range(1,5), pagination)

    def test_len_max_of_shows_in_pagination_if_is_less_than_middle(self):
        # Current page:3  - Qty pages: 4  - Middle pages: 3
        request_factory = RequestFactory()
        request = request_factory.get('home',data={'page':'24'})
        pagination = make_paginations(request, obj=list(range(1,160)), qty_options=6)
        # print(pagination['last_range']," / / ",pagination['middle_range']," / / ", request)
        self.assertLessEqual(pagination['current_page'],pagination['last_range'])

