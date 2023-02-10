from django.test import TestCase
import pytest
from farmacia.models import Category, Remedios, User
from utility.remediosautofill import factory


class BaseMixing:
    def make_medicine_no_defaults(self, qty=1):
        medicine = []
        for x in range(qty):
            resp = True
            dictionary = factory.make_medicine()
            if not medicine:  # this will avoid list out of index...
                medicine.append(self.make_medicines(**dictionary))
                resp = False
            if resp is True:
                for c in range(len(medicine)):
                    if str(dictionary['author_data']['username']) == str(medicine[c].author) or str(dictionary['slug']) == str(medicine[c].slug):
                        resp = False
            if resp is True:
                medicine.append(self.make_medicines(**dictionary))

        return medicine

    @staticmethod
    def make_category(name='Categoria'):
        return Category.objects.create(name=name)

    @staticmethod
    def make_author(first_name='user', last_name='name', username='username', password='123123',
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
        if author_data is None:
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
