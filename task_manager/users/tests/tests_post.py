import unittest
from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy
from task_manager.users.models import User
from django.contrib.messages import get_messages


class MyTestSuite(unittest.TestSuite):
    def __init__(self):
        super(MyTestSuite, self).__init__()
        self.addTest(SetUpTestCase('test_set_up'))
        self.addTest(UsersListTest('users_list_test'))
        self.addTest(UpdateUserTest('test_user_update_success'))
        self.addTest(DeleteUserTest('test_user_delete_success'))


class SetUpTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Andrey', last_name='Emelianenko',
            username='a_foaem'
        )
        self.user.set_password('asdaqwtWxow33L')
        self.user.save()

        self.client.login(
            username='a_foaem', password='asdaqwtWxow33L',
        )


class UsersListTest(TestCase):
    '''Test list of users, registry, login user.'''

    def test_index(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        c = Client()
        response = c.post('/users/create/', {
            'first_name': 'Andrey',
            'last_name': 'Totavich',
            'username': 'tota123',
            'password1': 'lexA456132',
            'password2': 'lexA456132',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_user(self):
        c = Client()
        response = c.post('/login/', {
            'username': 'tota123',
            'password': 'lexA456132',
        })
        self.assertEqual(response.status_code, 200)


class UpdateUserTest(SetUpTestCase):
    def test_user_update_success(self):
        response = self.client.post(
            reverse_lazy('user-update', kwargs={'pk': self.user.pk}),
            {'first_name': 'Adnrey', 'last_name': 'Emelianenko',
             'username': 'foaem_update', 'password1': 'asdaqwtWxow33L',
             'password2': 'asdaqwtWxow33L'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users-detail'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'User is successfully updated',
            'Пользователь успешно изменен',
        ])


class DeleteUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Jhon', last_name='Dhoe',
            username='junior_jhon'
        )
        self.user.set_password('qweRty123')
        self.user.save()

        self.client.login(
            username='junior_jhon', password='qweRty123',
        )

    def test_user_delete_success(self):
        response = self.client.post(
            reverse_lazy('user-delete', kwargs={'pk': self.user.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users-detail'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(str(messages[0]), [
            'User successfully deleted',
            'Пользователь успешно удален',
        ])


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(MyTestSuite())
