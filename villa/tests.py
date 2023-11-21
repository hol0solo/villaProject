from django.test import TestCase
from django.urls import reverse

from villa.models import Apartment, ApartmentCategory


class IndexViewTestCase(TestCase):

    def test_index(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertTemplateUsed('products/pre_order.html')
        self.assertEqual(response.status_code, 200)


class PropertiesListViewTestCase(TestCase):
    fixtures = ['apartmentcategory.json', 'apartment.json']

    def setUp(self) -> None:
        self.apartments = Apartment.objects.all()

    def test_apartments(self):
        path = reverse('villa:properties')
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context_data['apartments']), list(self.apartments[:3]))

    def test_apartments_category(self):
        category = ApartmentCategory.objects.first()
        path = reverse('villa:category', kwargs={'apartment_category_id': category.id})
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['apartments']),
            list(self.apartments.filter(category_id=category.id)[:3])
        )

    def _common_test(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('villa/properties.html')
        self.assertEqual(response.context_data['title'], 'Villa Agency - Property Listing by TemplateMo')
