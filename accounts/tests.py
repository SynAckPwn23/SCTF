from django.contrib.auth import get_user_model
from django.test import TestCase, Client, SimpleTestCase


class RegistrationTestCase(TestCase, SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.tmp_user = get_user_model().objects.create_user(
            'temporary',
            'temporary@gmail.com',
            'temporary'
        )


    #Test User Login
    def test_login(self):
        response = self.client.post('/accounts/login/', {
            'username': 'username',
            'password': 'u1u2u3u4',
            })
        u = get_user_model().objects.first()
        # Correct username and password
        self.assertEqual(u.username, 'username')
        self.assertEqual(u.password, 'u1u2u3u4')
        self.assertEqual(response.status_code, 200)

    #Test User Login Empty
    def test_login_empty(self):
        response = self.client.post('/accounts/login/', {
            'username': 'username',
            'password': 'u1u2u3u4',
            })
        u = get_user_model().objects.first()
        # Correct username and password
        self.assertEqual(u.username, '')
        self.assertEqual(u.password, '')
        self.assertIn('This value is required.', response.content)

    #Test Reset Password
    def test_reset(self):
        response = self.client.post('/accounts/password/reset', {
            'email': 'username@username.it',
            })
        u = get_user_model().objects.first()
        # Correct email
        self.assertEqual(u.email, 'username@username.it')
        self.assertEqual(response.status_code, 200)

    #Test Reset Password Empty
    def test_reset_empty(self):
        response = self.client.post('/accounts/password/reset', {
            'email': 'username@username.it',
            })
        u = get_user_model().objects.first()
        # Wrong email
        self.assertEqual(u.email, '')
        self.assertIn('This value is required.', response.content)

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
        # Created
        self.assertEqual(response.status_code, 302)

        u = get_user_model().objects.last()
        # Correct username
        self.assertEqual(u.username, 'username')
        # Correct email
        self.assertEqual(u.email, 'username@username.it')
        # Correct first_name
        self.assertEqual(u.first_name, 'FirstName')
        # Correct last_name
        self.assertEqual(u.last_name, 'LastName')


    #Test User Registration Empty
    def test_register_empty(self):
        response = self.client.post('/accounts/register/', {
            'username': 'username',
            'email': 'username@username.it',
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'password1': 'u1u2u3u4',
            'password2': 'u1u2u3u4',
            })
        u = get_user_model().objects.first()
        # Empty username
        self.assertEqual(u.username, '')
        # Empty email
        self.assertEqual(u.email, '')
        # Empty first_name
        self.assertEqual(u.first_name, '')
        # Empty last_name
        self.assertEqual(u.last_name, '')
        # Empty password1
        self.assertEqual(u.password1, '')
        # Empty pasword2
        self.assertEqual(u.password2, '')
        self.assertIn('This value is required.', response.content)


    def test_login_without_profile(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn('User without profile', response.content)


