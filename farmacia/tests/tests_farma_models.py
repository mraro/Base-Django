import pytest

from .tests_medicine_base import BaseTestMedicine
from django.core.exceptions import ValidationError
from parameterized import parameterized


@pytest.mark.objects
class Tests_Models_Remedios(BaseTestMedicine):
    def setUp(self) -> None:  # SETUP WILL REPRODUCE BEFORE, IN EVERY funcions IN THIS class
        self.medicine = self.make_medicine_no_defaults()[0]  # WILL MAKE A DATA TO TEST
        self.medicine.is_published = False  # MODELING DATA
        self.medicine.full_clean()  # TESTS IF IS PROPERLY TO SAVE
        self.medicine.save()
        return super().setUp()

    def test_farma_title_has_len_smaller_than_max_size_of_db(self):
        self.medicine.title = 'A' * 66

        with self.assertRaises(ValidationError):  # RETURN ERROR IF TITLE HAS MORE THAN IS POSSIBLE
            self.medicine.full_clean()  # THIS MAKE TEST OF ALL PROPERTIES IN MODELS DB

        self.medicine.save()

    def test_limit_of_inputs_for_db(self):
        setattr(self.medicine, 'title', "A" * 66)
        with self.assertRaises(ValidationError):
            self.medicine.full_clean()

    def test_boolean_if_medicine_has_false_as_default(self):
        novo_remedio = self.medicine
        self.assertFalse(
            novo_remedio.is_published,
            msg="Medicine hasn't been deployed"
        )

    def test_medicine_string_title_representatios(self):
        self.medicine.title = "TEST is the Same"
        self.medicine.full_clean()
        self.medicine.save()
        self.assertEqual(str(self.medicine), "TEST is the Same", msg="Erro,string representation isn't the same title")
