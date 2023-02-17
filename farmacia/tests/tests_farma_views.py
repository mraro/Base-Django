import pytest
from django.urls import reverse, resolve
from unittest import skip
from farmacia import views
from .tests_medicine_base import BaseTestMedicine, TestCase


# METODOLOGIA TDD, CRIA O TESTE DEPOIS O CODIGO ( TEST DRIVEN DEVELOPMENT )
@pytest.mark.objects
class RemedioViewsHomeTest(BaseTestMedicine):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_farma_view_home_is_correct(self):
        view_resolve = resolve(reverse('farmacia:home'))
        self.assertIs(view_resolve.func, views.home)

    def test_farma_view_home_response_code_200_is_ok(self):
        response = self.client.get(reverse('farmacia:home'))
        self.assertEqual(response.status_code, 200)

    def test_farma_view_home_template_loads_properly(self):
        response = self.client.get(reverse('farmacia:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    @skip("Pulando teste pois temos uma receita")
    def test_farma_view_home_template_has_NO_medicines(self):
        self.make_medicines(is_published=False)
        response = self.client.get(reverse('farmacia:home'))
        self.assertIn('<h1> Sem Estoque </h1>', response.content.decode('utf-8'))

    def test_farma_view_home_template_loading_medicines(self):
        self.make_medicines(author_data={
            'first_name': "Joaozinho"
        })
        response = self.client.get(reverse('farmacia:home'))
        content = response.content.decode('utf-8')  # SITE rendenizado ( o bruto html)
        context = response.context['remedios']  # VARIAVEIS retornadas do site <QuerySet [<Remedios: value Title>]>
        self.assertIn('value Title', content)
        self.assertIn('Joaozinho', content)
        self.assertEqual(len(context), 1)


@pytest.mark.objects
class RemedioViewsSearchTest(BaseTestMedicine):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_farma_view_search_is_correct(self):
        resolved = resolve(reverse('farmacia:search'))
        self.assertIs(resolved.func, views.search)

    def test_farma_view_search_loads_correct_template(self):
        response = self.client.get(reverse('farmacia:search') + '?q=teste')
        self.assertTemplateUsed(response, 'pages/search.html')

    def test_farma_view_search_term_is_on_page(self):
        url = reverse('farmacia:search') + '?q=teste'
        response = self.client.get(url)
        self.assertIn('Nenhum resultado encontrado sobre teste', response.content.decode('utf-8'))

    def test_farma_view_search_by_title_is_ok(self):
        self.make_medicines(title="teste de pesquisa")
        response = self.client.get(reverse('farmacia:search') + "?q=teste")
        self.assertIn("teste de pesquisa", response.content.decode('utf-8'))

    def test_farma_view_search_by_description_is_ok(self):
        self.make_medicines(author_data={'username': "Tu"},
                            title="pesquisa1", description="decrição teste", slug="unique1")
        self.make_medicines(author_data={'username': "Nos"},
                            title="pesquisa2", description="decrição teste", slug="unique2")

        response = self.client.get(reverse('farmacia:search') + "?q=teste")
        self.assertIn("pesquisa1", response.content.decode('utf-8'))  # assert in title because I don't show description
        self.assertIn("pesquisa2", response.content.decode('utf-8'))  # assert in title because I don't show description

    def test_farma_view_serach_if_var_q_is_empty_and_return_error_404(self):
        response = self.client.get(reverse('farmacia:search') + '?q=')
        self.assertEqual(response.status_code, 404)


@pytest.mark.objects
class RemedioViewsRemedioTest(BaseTestMedicine):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_farma_view_remedio_is_correct(self):
        view_resolve = resolve(reverse('farmacia:remedio', args=[1]))
        self.assertIs(view_resolve.func, views.remedios)

    def test_farma_view_remedio_response_code_404(self):
        response = self.client.get(reverse('farmacia:remedio', args=[100]))
        self.assertEqual(response.status_code, 404)

    def test_farma_view_remedio_if_template_loads_properly(self):
        self.make_medicine_no_defaults()
        response = self.client.get(reverse('farmacia:remedio', kwargs={'idremedios': 1}))
        self.assertTemplateUsed(response, 'pages/remedio-view.html')


@pytest.mark.objects
class RemedioViewsCategoryTest(BaseTestMedicine):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_farma_view_category_is_correct(self):
        view_resolve = resolve(reverse('farmacia:categoria', kwargs={'idcategoria': 1}))
        self.assertIs(view_resolve.func, views.categoria)

    def test_farma_view_category_response_code_404(self):
        response = self.client.get(reverse('farmacia:categoria', kwargs={'idcategoria': 1}))
        self.assertEqual(response.status_code, 404)

    def test_farma_view_category_if_template_loads_properly(self):
        self.make_medicine_no_defaults()
        response = self.client.get(reverse('farmacia:categoria', kwargs={'idcategoria': 1}))
        self.assertTemplateUsed(response, 'pages/category-view.html')


@pytest.mark.objects
class AuthorsViewRegisterTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_author_view_register_if_template_loads_properly(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'pages/register_view.html')
