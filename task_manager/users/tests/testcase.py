from django.test import TestCase, Client
from task_manager.users.models import User
import json
import os


def load_data(path):
    with open(os.path.abspath(f'task_manager/fixtures/{path}'), 'r') as file:
        return json.loads(file.read())


class UserTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']
    test_user = load_data('test_users.json')

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(pk=1)
        
        self.user2 = User.objects.get(pk=2)
        
        self.user3 = User.objects.get(pk=3)
        
        self.users = User.objects.all()
        self.count = User.objects.count()
