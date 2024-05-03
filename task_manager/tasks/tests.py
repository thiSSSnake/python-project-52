from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from task_manager.users.models import User
from task_manager.statuses.models import Status
from .models import Task
# Create your tests here.


class SetUpTestCase(TestCase):
    def setUp(self):
        # Create user author
        self.user = User.objects.create(
            first_name='Tony', last_name='Soprano',
            username='boss_of_newark',
        )
        self.user.set_password('dqweRty21')
        self.user.save()

        # Create user executor
        self.user2 = User.objects.create(
            first_name='Cris', last_name='Moltisanti',
            username='real_og',
        )
        self.user2.set_password('Alsfkqwo21')
        self.user2.save()

        # Create status

        self.status = Status.objects.create(name='status')
        self.status.save()

        # Create task
        self.task = Task.objects.create(
            name='go to home',
            body='a need to go home',
            status=Status.objects.get(pk=self.status.pk),
            executor=User.objects.get(pk=self.user.pk),
            author=self.user
            )
        
        self.task.save()

        self.status2 = Status.objects.create(name='new_status')
        self.status2.save()
        self.client.login(
            username='boss_of_newark', password='dqweRty21',
        )


class TaskCreateTest(SetUpTestCase):

    def test_task_create_success_view(self):
        response = self.client.get(reverse_lazy('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')


    def test_task_create_success(self):
        response = self.client.post(reverse_lazy('task_create'), {
            'name': 'bbb',
            'body': 'xxczczc',
            'status': self.status.id,
            'executor': self.user2.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Task successfully created',
            'Задача успешно создана',
        ])
        new_task = Task.objects.get(name='bbb')
        self.assertIsNotNone(new_task)


class TaskUpdateTest(SetUpTestCase):

    def test_task_update_view(self):
        response = self.client.get(reverse_lazy('task_update', kwargs={'pk':self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')
    
    def test_task_update_success(self):
        response = self.client.post(reverse_lazy('task_update', kwargs={'pk':self.task.pk}), {
            'name':'go to badabing',
            'body':'im on work',
            'status': self.status2.id,
            'executor': self.user.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Task successfully updated',
            'Задача успешно обновлена',
        ])


class TaskDeleteTest(SetUpTestCase):

    def test_task_delete_view(self):
        response = self.client.get(reverse_lazy('task_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/delete.html')

    def test_task_delete_success(self):
        response = self.client.post(reverse_lazy('task_delete', kwargs={'pk': self.task.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'Task successfully deleted',
            'Задача успешно удалена',
        ])

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=1)
