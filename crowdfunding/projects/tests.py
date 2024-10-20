from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Pledge

class PledgeDetailTestCase(TestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Create pledges
        self.pledge1 = Pledge.objects.create(amount=100, supporter=self.user1)
        self.pledge2 = Pledge.objects.create(amount=200, supporter=self.user2)

        # Create API client
        self.client = APIClient()

    def test_get_pledge_as_supporter(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Attempt to get pledge1
        response = self.client.get(f'/pledges/{self.pledge1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pledge_as_non_supporter(self):
        # Log in as user2
        self.client.login(username='user2', password='password2')

        # Attempt to get pledge1
        response = self.client.get(f'/pledges/{self.pledge1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_pledge_as_supporter(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Attempt to update pledge1
        response = self.client.put(f'/pledges/{self.pledge1.pk}/', {'amount': 150})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pledge1.refresh_from_db()
        self.assertEqual(self.pledge1.amount, 150)

    def test_put_pledge_as_non_supporter(self):
        # Log in as user2
        self.client.login(username='user2', password='password2')

        # Attempt to update pledge1
        response = self.client.put(f'/pledges/{self.pledge1.pk}/', {'amount': 150})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)