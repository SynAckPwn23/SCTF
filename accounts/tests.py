from django.contrib.auth import get_user_model
from django.test import TestCase, Client



class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    #Test User Login
    def test_login(self):
        response = self.client.post('/accounts/login/', {
            'username': 'username',
            'password': 'u1u2u3u4',
            })
        u = get_user_model().objects.first()
        self.assertEqual(u.username, 'username')
        self.assertEqual(u.password, 'u1u2u3u4')
        self.assertEqual(response.status_code, 200)


    #Test User Registration
    def test_register(self):
        response = self.client.post('/accounts/register/', {
            'username': 'username',
            'email': 'username@username.it',
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'password1': 'u1u2u3u4',
            'password2': 'u1u2u3u4',
            })
        u = get_user_model().objects.first()
        self.assertEqual(u.username, 'username')
        self.assertEqual(u.email, 'username@username.it')
        self.assertEqual(u.first_name, 'FirstName')
        self.assertEqual(u.last_name, 'LastName')
        self.assertEqual(u.password1, 'u1u2u3u4')
        self.assertEqual(u.password2, 'u1u2u3u4')
        self.assertEqual(response.status_code, 200)


    
