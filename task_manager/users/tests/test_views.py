from django.urls import reverse_lazy
from .testcase import UserTestCase


class TestUserList(UserTestCase):
    def test_users_view(self):
        response = self.client.get(reverse_lazy('users-detail'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='users/index.html'
        )

    def test_users_content(self):
        response = self.client.get(reverse_lazy('users-detail'))

        self.assertEqual(len(response.context['users']), self.count)
        self.assertQuerysetEqual(
            response.context['users'],
            self.users,
            ordered=False
        )

    def test_users_links(self):
        response = self.client.get(reverse_lazy('users-detail'))

        self.assertContains(response, '/users/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/users/{pk}/update/')
            self.assertContains(response, f'/users/{pk}/delete/')


class TestCreateUserView(UserTestCase):
    def test_create_user_view(self):
        response = self.client.get(reverse_lazy('users-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')


class TestUpdateUserView(UserTestCase):
    def test_update_user_view(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse_lazy('user-update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/update.html')

    def test_update_not_logged_in_view(self):
        self.client.logout()

        response = self.client.get(
            reverse_lazy('user-update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestDeleteUserView(UserTestCase):
    def test_delete_user_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy('user-delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')

    def test_delete_task_not_logged_in_view(self):
        self.client.logout()

        response = self.client.get(
            reverse_lazy('user-delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_task_unauthorised_view(self):
        response = self.client.get(
            reverse_lazy('user-delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
