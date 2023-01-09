from django.urls import reverse, resolve
from unittest import skip
from farmacia import views
from .tests_medicine_base import BaseTestMedicine

# METODOLOGIA TDD, CRIA O TESTE DEPOIS O CODIGO
class RemedioViewsTest(BaseTestMedicine):
    def test_farma_view_home_is_correct(self):
        view_resolve = resolve(reverse('farmacia:home'))
        self.assertIs( view_resolve.func, views.home)

    def test_farma_home_response_code_200_is_ok(self):
        response = self.client.get(reverse('farmacia:home'))
        self.assertEqual(response.status_code , 200)

    def test_farma_home_template_loads_properly(self):
        response = self.client.get(reverse('farmacia:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    @skip("Pulando teste pois temos uma receita")
    def test_farma_home_template_has_NO_medicines(self):
        self.make_medicines(is_published=False)
        response = self.client.get(reverse('farmacia:home'))
        self.assertIn('<h1> Sem Estoque </h1>' , response.content.decode('utf-8'))

    def test_farma_home_template_loading_medicines(self):
        self.make_medicines(author_data={
            'first_name' : "Joaozinho"
        })
        response = self.client.get(reverse('farmacia:home'))
        content = response.content.decode('utf-8') # SITE rendenizado ( o bruto html)
        context = response.context['remedios'] # VARIAVEIS retornadas do site <QuerySet [<Remedios: value Title>]>
        self.assertIn('value Title', content)
        self.assertIn('Joaozinho', content)
        self.assertEqual(len(context), 1)


    def test_farma_view_remedio_is_correct(self):
        view_resolve = resolve(reverse('farmacia:remedio', args=[1]))
        self.assertIs( view_resolve.func, views.remedios)

    def test_farma_view_remedio_response_code_404(self):
        response = self.client.get(reverse('farmacia:remedio', args=[100]))
        self.assertEqual(response.status_code , 404)


    def test_farma_view_category_is_correct(self):
        view_resolve = resolve(reverse('farmacia:categoria', kwargs={'idcategoria': 1}))
        self.assertIs( view_resolve.func, views.categoria)

    def test_farma_view_category_response_code_404(self):
        response = self.client.get(reverse('farmacia:categoria', kwargs={'idcategoria': 1000}))
        self.assertEqual(response.status_code , 404)

