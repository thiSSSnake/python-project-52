# Test for POST methods app tasks
from django.urls import reverse_lazy
from .testcase import TaskTestCase
from task_manager.tasks.models import Task


class TestCreateTask(TaskTestCase):
    def test_create_valid_task(self):
        task_data = self.test_task['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(
            Task.objects.last().name,
            task_data['name']
        )
        self.assertEqual(
            Task.objects.last().author,
            self.user1
        )
        self.assertEqual(
            Task.objects.last().executor,
            self.user2
        )


class TestUpdateTask(TaskTestCase):
    def test_update_task(self):
        task_data = self.test_task['update'].copy()
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        self.assertEqual(Task.objects.count(), self.count)
        self.assertEqual(
            Task.objects.get(id=self.task2.id).name,
            task_data['name']
        )
        self.assertEqual(
            Task.objects.get(id=self.task2.id).executor.id,
            task_data['executor']
        )


class TestDeleteTask(TaskTestCase):
    def test_delete_task(self):
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        self.assertEqual(Task.objects.count(), self.count - 1)
