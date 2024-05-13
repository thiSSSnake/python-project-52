# Test for POST methods app tasks
from django.urls import reverse_lazy
from .testcase import UserTestCase
from task_manager.users.models import User


class TestUserCreate(UserTestCase):
    def test_create_valid_user(self):
        user_data = self.test_user['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('users-create'),
            data=user_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(
            User.objects.last().username,
            user_data['username']
        )


class TestUpdateUser(UserTestCase):
    def test_update_user(self):
        self.client.force_login(self.user2)

        user_data = self.test_user['update'].copy()
        response = self.client.post(
            reverse_lazy('user-update', kwargs={'pk': self.user2.pk}),
            data=user_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users-detail'))

        self.assertEqual(User.objects.count(), self.count)
        self.assertEqual(
            User.objects.get(id=self.user2.id).first_name,
            user_data['first_name']
        )


class TestDeleteUser(UserTestCase):
    def test_delete_user(self):
        self.client.force_login(self.user3)
        response = self.client.post(
            reverse_lazy('user-delete', kwargs={'pk': 3})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users-detail'))

        self.assertEqual(User.objects.count(), self.count - 1)