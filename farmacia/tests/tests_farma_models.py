from .tests_medicine_base import BaseTestMedicine
from django.core.exceptions import ValidationError


class Tests_Models(BaseTestMedicine):
    def setUp(self) -> None:
        self.medicine = self.make_medicines()
        return super().setUp()

    def test_farma_title_has_len_smaller_than_max_size_of_db(self):
        self.medicine.title = 'A' * 66

        with self.assertRaises(ValidationError):  # RETURN ERROR IF TITLE HAS MORE THAN IS POSSIBLE
            self.medicine.full_clean()  # THIS MAKE TEST OF ALL PROPERTIES IN MODELS DB

        self.medicine.save()
