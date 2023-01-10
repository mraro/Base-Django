from django.test import TestCase
from django.urls import reverse



class RemedioURLsTest(TestCase):
    def test_farma_url_home_is_correct(self):
        home_url = reverse('farmacia:home')
        self.assertEqual(home_url, '/')

    def test_farma_url_remedio_is_correct(self):
        url = reverse('farmacia:remedio', args=[1])
        self.assertEqual(url, "/remedios/1/")

    def test_farma_url_category_is_correct(self):
        url = reverse('farmacia:categoria', kwargs={'idcategoria': 1})
        self.assertEqual(url, "/category/1/")

    def test_farma_url_search_is_correct(self):
        url = reverse('farmacia:search')
        self.assertEqual(url, "/search/")