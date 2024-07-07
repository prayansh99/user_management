from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

class SignupViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('register_user')
        self.valid_payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe8',
            'email': 'johndoe8@example.com',
            'password': 'password123'
        }

    def test_signup_valid_data(self):
        valid_payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe16',
            'email': 'johndoe16@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.signup_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_invalid_data(self):
        valid_payload = {
            'first_name': 'John4',
            'last_name': 'Doe',
            'username': 'johndoe10',
            'email': 'johndoe10@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.signup_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalid_data2(self):
        valid_payload = {
            'first_name': 'John4',
            'last_name': 'Doe',
            'username': 'johndoe10',
            'email': 'johndoe20@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.signup_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalid_data3(self):
        valid_payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe20',
            'email': 'johndoe10@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.signup_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_existing_user(self):
        # Create a user first
        # User.create_user(valid_payload)

        response = self.client.post(self.signup_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User with this email or username already exists.', response.data['error'])

    def test_signup_empty_payload(self):
        response = self.client.post(self.signup_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Request body cannot be empty', response.data['error'])

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'johndoe@example.com',
            'password': 'password123'
        }
        self.invalid_credentials = {
            'email': 'johndoe@example.com',
            'password': 'wrongpassword'
        }

    def test_login_valid_credentials(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('user_id', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, self.invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid credentials', response.data['error'])

    def test_login_empty_payload(self):
        response = self.client.post(self.login_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Request body cannot be empty', response.data['error'])

class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('logout')

    def test_logout(self):
        # Perform login to set the cookie
        login_url = reverse('login')
        login_data = {'email': 'johndoe@example.com', 'password': 'password123'}
        login_response = self.client.post(login_url, login_data, format='json')

        # Now perform logout
        self.client.credentials(HTTP_USER_ID=login_response.data['user_id'])
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Successfully logged out', response.data['message'])

    def test_logout_without_login(self):
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Or you can handle this differently


from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class UserDetailViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()


    def test_get_user_details(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe8',
            'email': 'johndoe8@example.com',
            'password': 'password123'
        }

        # login a user
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with user_id in the header
        self.client.credentials(HTTP_USER_ID=user_id)

        # Make the user detail request
        response = self.client.get(f'/user/user_profile/{user_id}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)

    def test_get_user_details_invalid_id(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe7',
            'email': 'johndoe7@example.com',
            'password': 'password123'
        }
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)


        # Make a user detail request with an invalid user_id
        invalid_user_id = 'invaliduserid'
        response = self.client.get(f'/user/user_profile/{invalid_user_id}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_user_details_invalid_id2(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe7',
            'email': 'johndoe7@example.com',
            'password': 'password123'
        }
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)


        # Make a user detail request with an invalid user_id
        invalid_user_id = 'invaliduserid@'
        response = self.client.get(f'/user/user_profile/{invalid_user_id}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_user_details_invalid_id3(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe7',
            'email': 'johndoe7@example.com',
            'password': 'password123'
        }
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)


        # Make a user detail request with an invalid user_id
        invalid_user_id = 'invalidid'
        response = self.client.get(f'/user/user_profile/{invalid_user_id}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_user_details_invalid_id4(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe7',
            'email': 'johndoe7@example.com',
            'password': 'password123'
        }
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)


        # Make a user detail request with an invalid user_id
        invalid_user_id = None
        response = self.client.get(f'/user/user_profile/{invalid_user_id}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class UserDetailByUsernameViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_user_details_by_username(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe4',
            'email': 'johndoe4@example.com',
            'password': 'password123'
        }
        # Register and login a user
        self.client.post('/register_user', user_data, format='json')
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)

        # Make a user detail request by username
        response = self.client.get(f'/user/user_profile/username/{user_data["username"]}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)

    def test_get_user_details_by_invalid_username(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe3',
            'email': 'johndoe3@example.com',
            'password': 'password123'
        }
        # Register and login a user
        self.client.post('/register_user', user_data, format='json')
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)

        # Make a user detail request with an invalid username
        invalid_username = 'invalid_username@'
        response = self.client.get(f'/user/user_profile/username/{invalid_username}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_user_details_by_invalid_username2(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe3',
            'email': 'johndoe3@example.com',
            'password': 'password123'
        }
        # Register and login a user
        self.client.post('/register_user', user_data, format='json')
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)

        # Make a user detail request with an invalid username
        invalid_username = 'invalid_user'
        response = self.client.get(f'/user/user_profile/username/{invalid_username}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_user_details_by_invalid_username3(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe3',
            'email': 'johndoe3@example.com',
            'password': 'password123'
        }
        # Register and login a user
        self.client.post('/register_user', user_data, format='json')
        login_data = {'email': user_data['email'], 'password': user_data['password']}
        login_response = self.client.post(reverse('login'), login_data, format='json')

        # Extract user_id and access token from login response
        user_id = login_response.data['user_id']
        print(user_id)
        # Set credentials with access token in the header
        self.client.credentials(HTTP_USER_ID=user_id)

        # Make a user detail request with an invalid username
        invalid_username = None
        response = self.client.get(f'/user/user_profile/username/{invalid_username}', format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)





