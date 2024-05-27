from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from task_manager.users.models import User
from .models import Status
# Create your tests here.


class SetUpTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Tony', last_name='Soprano',
            username='boss_of_newark',
        )
        self.user.set_password('dqweRty21')
        self.user.save()

        self.status = Status.objects.create(name='status')
        self.status.save()

        self.status2 = Status.objects.create(name='status2')
        self.status2.save()
        self.client.login(
            username='boss_of_newark', password='dqweRty21',
        )


class StatusCreateTest(SetUpTestCase):
    def test_status_create_success(self):
        response = self.client.post(
            reverse_lazy('statuses-create'),
            {'name': 'new_status'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses-detail'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Status successfully added',
            'Статус успешно создан',
        ])
        new_status = Status.objects.get(name='new_status')
        self.assertIsNotNone(new_status)


class StatusUpdateTest(SetUpTestCase):
    def test_status_update_view(self):
        response = self.client.get(reverse_lazy('status-update',
                                                kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/update.html')

    def test_status_update_success(self):
        response = self.client.post(
            reverse_lazy('status-update', kwargs={'pk': self.status.pk}),
            {'name': 'old_status'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses-detail'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Status successfully changed',
            'Статус успешно изменен',
        ])


class StatusDeleteTestCase(SetUpTestCase):
    def test_status_delete_view(self):
        response = self.client.get(reverse_lazy(
            'status-delete', kwargs={'pk': self.status.pk}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/delete.html')

    def test_status_delete_success(self):
        response = self.client.post(
            reverse_lazy('status-delete', kwargs={'pk': self.status.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses-detail'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Status successfully deleted',
            'Статус успешно удален',
        ])

        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=1)
