from django.test import TestCase
import pytest
from farmacia.models import Category, Remedios, User
from utility.remediosautofill import factory


class BaseMixing:
    def make_medicine_no_defaults(self, qty=1):
        medicine = []
        for x in range(qty):
            dictionary = factory.make_medicine_db()
            medicine.append(self.make_medicines(**dictionary))
        return medicine

    def make_category(self, name='Categoria'):
        return Category.objects.create(name=name)

    def make_author(self, first_name='user', last_name='name', username='username', password='123123',
                    email='user@mail.com', ):  # noqa: E501
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_medicines(self, category='CategoriaIn', author_data=None, title='value Title', description='value',
                       slug='value', price=10.10,
                       preparetion_steps='value', preparetion_steps_is_html=True, is_published=True, ):
        if author_data == None:
            author_data = {}

        return Remedios.objects.create(
            category=self.make_category(category),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            price=price,
            preparetion_steps=preparetion_steps,
            preparetion_steps_is_html=preparetion_steps_is_html,
            is_published=is_published,
        )


@pytest.mark.medicine
class BaseTestMedicine(TestCase, BaseMixing):
    def setUp(self) -> None:
        # category = Category(name='Categoria')
        # category.save()
        # self.make_medicines()

        return super().setUp()
