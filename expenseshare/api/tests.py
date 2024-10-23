from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Expense
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class ExpenseViewSetTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            name='User One',
            mobile_number='1234567890',
          
             
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            name='User Two',
            mobile_number='0987654321',
          
        )
        self.user3 = User.objects.create_user(
            email='user3@example.com',
            name='User Three',
            mobile_number='1122334455',
            
        )
        print(self.user1)
        
        self.token_url = reverse('token_obtain_pair')
        response = self.client.post(self.token_url, {
            'username': self.user1,
            'password': "",
        })
        print(response.data)
        token = response.data['access'] 

     
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')



   
    def test_create_expense_equal_split(self):
        # Test equal split
        url = reverse('expense-list')  
        data = {
            'description': 'Lunch',
            'amount': 60.0,
            'participants': [self.user1.id, self.user2.id],
            'split_method': 'equal',
             'split_details': []
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['split_details']), 2)
        self.assertEqual(response.data['split_details'][0]['amount'], 30.0)

    def test_create_expense_exact_split(self):
        # Test exact split
        url = reverse('expense-list')
        data = {
            'description': 'Dinner',
            'amount': 100.0,
            'participants': [self.user1.id, self.user2.id],
            'split_method': 'exact',
            'split_details': [40, 60]
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['split_details'][0]['amount'], 40.0)
        self.assertEqual(response.data['split_details'][1]['amount'], 60.0)

    def test_create_expense_percentage_split(self):
        # Test percentage split
        url = reverse('expense-list')
        data = {
            'description': 'Group Dinner',
            'amount': 200.0,
            'participants': [self.user1.id, self.user2.id],
            'split_method': 'percentage',
            'split_details': [60, 40]  # 60% for user1, 40% for user2
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['split_details'][0]['amount'], 120.0)
        self.assertEqual(response.data['split_details'][1]['amount'], 80.0)

    def test_create_expense_invalid_percentage_split(self):
        # Test invalid percentage (sum != 100)
        url = reverse('expense-list')
        data = {
            'description': 'Invalid Dinner',
            'amount': 200.0,
            'participants': [self.user1.id, self.user2.id],
            'split_method': 'percentage',
            'split_details': [70, 40]  # Invalid sum (70+40 != 100)
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Percentages must add up to 100%')
