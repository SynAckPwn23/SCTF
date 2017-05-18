from django.contrib.auth import get_user_model
from django.test import TestCase, Client



class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.post('/accounts/register/', {
            'username': 'username',
            'email': 'username@username.it',
            'password1': 'u1u2u3u4',
            'password2': 'u1u2u3u4',
            'first_name': 'UserName'
        })
        u = get_user_model().objects.first()
        self.assertEqual(u.username, 'username')
        self.assertEqual(u.first_name, 'UserName')
