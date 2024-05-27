# Test views & html templates
from django.urls import reverse_lazy
from .testcase import TaskTestCase


class TestListTasks(TaskTestCase):
    def test_tasks_view(self):
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks/index.html'
        )

    def test_tasks_content(self):
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(len(response.context['tasks']), self.count)
        self.assertQuerysetEqual(
            response.context['tasks'],
            self.tasks,
            ordered=False
        )

    def test_tasks_links(self):
        response = self.client.get(reverse_lazy('tasks'))

        self.assertContains(response, '/tasks/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/tasks/{pk}/update/')
            self.assertContains(response, f'/tasks/{pk}/delete/')

    def test_tasks_not_logged_in_view(self):
        self.client.logout()

        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestFilterTaskView(TaskTestCase):
    def test_task_filter_status(self):
        response = self.client.get(reverse_lazy('tasks'),
                                   {"status": self.status1.pk})
        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)

    def test_task_filter_executor(self):
        response = self.client.get(reverse_lazy('tasks'),
                                   {"executor": self.user1.pk})
        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertNotContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_task_filter_label(self):
        response = self.client.get(reverse_lazy('tasks'),
                                   {"labels": self.label2.pk})
        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertNotContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_task_own_filter(self):
        response = self.client.get(reverse_lazy('tasks'), {"own_tasks": "on"})
        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)


class TestCreateTaskView(TaskTestCase):
    def test_create_task_view(self):
        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/create.html')

    def test_create_task_not_logged_in_view(self):
        self.client.logout()

        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestUpdateTaskView(TaskTestCase):
    def test_update_task_view(self):
        response = self.client.get(
            reverse_lazy('task_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/update.html')

    def test_update_not_logged_in_view(self):
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestDeleteTaskView(TaskTestCase):
    def test_delete_task_view(self):
        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/delete.html')

    def test_delete_task_not_logged_in_view(self):
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_task_unauthorised_view(self):
        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
