from django.test import TestCase
from django.urls import reverse
from .models import Status, Applications
from cheklist.forms import AplicationsForm

class StatusModelTest(TestCase):
    def test_status_str_representation(self):
        status = Status.objects.create(status='Оформлено')
        self.assertEqual(str(status), 'Оформлено')

class ApplicationsModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(status='Оформлено')

    def test_application_absolute_url(self):
        application = Applications.objects.create(
            status_id=self.status,
            bx_id=1,
            planup_id=2,
            user_id=3,
            slug='slug-1'
        )
        expected_url = reverse('update_application_info', kwargs={'application_slug': application.slug})
        self.assertEqual(application.get_absolute_url(), expected_url)

class ViewsTest(TestCase):
    def update_application(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Welcome to our website')



class FormTest(TestCase):
    def setUp(self):
        # Создаем статус с id=2
        Status.objects.create(status='В процессе')

    def test_valid_form(self):
        data = {'status_id': 2, 'bx_id': 1,'planup_id':2,'user_id':2,'slug':'slug-1'}
        form = AplicationsForm(data=data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())





