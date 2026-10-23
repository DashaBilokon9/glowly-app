from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from salon.forms import AppointmentForm
from salon.models import Service, Specialist


class AppointmentFormTests(TestCase):
    def setUp(self):
        self.manicure = Service.objects.create(
            name='Манікюр',
            price='450.00',
            duration_minutes=60,
        )
        self.haircut = Service.objects.create(
            name='Стрижка',
            price='500.00',
            duration_minutes=45,
        )
        self.olena = Specialist.objects.create(name='Олена')
        self.olena.services.add(self.manicure)

    def _data(self, service):
        starts_at = timezone.localtime(timezone.now() + timedelta(days=1))
        return {
            'service': service.pk,
            'specialist': self.olena.pk,
            'client_name': 'Ірина',
            'client_phone': '0501234567',
            'starts_at': starts_at.strftime('%Y-%m-%dT%H:%M'),
        }

    def test_rejects_specialist_without_service(self):
        form = AppointmentForm(data=self._data(self.haircut))
        self.assertFalse(form.is_valid())

    def test_accepts_matching_service(self):
        form = AppointmentForm(data=self._data(self.manicure))
        self.assertTrue(form.is_valid())


class IntroPageTests(TestCase):
    def test_home_is_intro_and_catalog_lists_services(self):
        Service.objects.create(name='Манікюр', price='450.00', duration_minutes=60)
        home = self.client.get('/')
        catalog = self.client.get('/catalog/')
        self.assertContains(home, 'Як записатися')
        self.assertContains(catalog, 'Манікюр')

    def test_english_button_translates_page_and_service_name(self):
        Service.objects.create(
            name='Манікюр',
            name_en='Manicure',
            price='450.00',
            duration_minutes=60,
        )
        self.client.post('/i18n/setlang/', {'language': 'en', 'next': '/'})
        home = self.client.get('/')
        self.assertContains(home, 'How to book')
        self.assertContains(home, 'Manicure')
