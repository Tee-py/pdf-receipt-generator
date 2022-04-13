from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import User
from ..constants import ErrorCodes
import json


# Create your tests here.

class Test(APITestCase):

    def setUp(self):
        
        self.user_data = {
            "email": "testuser@gmail.com",
            "password": "test"
        }
        self.user = User.objects.create_user(**self.user_data)

        self.login_route = reverse("login")
        self.refresh_route = reverse("token_refresh")
        self.create_user_route = reverse("create_user")
        self.receipt_route = reverse("receipt")
        return super().setUp()
    
    def test_login_and_token_refresh(self):
        # Login With Wrong Credentials
        resp = self.client.post(self.login_route, {"email": "wrong@mail.com", "password": "wrong"})
        self.assertEqual(resp.status_code, 401)

        # Login With Correct Credentials
        resp = self.client.post(self.login_route, self.user_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('refresh', resp.json())
        self.assertIn('access', resp.json())

        #Test Token Refresh
        refresh_payload = {
            "refresh": resp.json()['refresh']
        }
        resp = self.client.post(self.refresh_route, refresh_payload)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.json())
    
    def test_create_user(self):
        # Wrong Data Test
        resp = self.client.post(self.create_user_route, {"email": "hello", "password": "hiii"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['error_code'], ErrorCodes.VALIDATION_ERROR.value)

        # Create User Test
        resp = self.client.post(self.create_user_route, {"email": "bukky@gmail.com", "password": "password"})
        self.assertEqual(resp.status_code, 201)

    def test_generate_receipt(self):
        data = {
            "company_name": "FlashPay Inc",
            "company_address": "23, London Avenue, Ayetoro, Germany.",
            "receipt_id": "RECP-287657",
            "customer_name": "Emmanuel Oluwatobi",
            "customer_email": "emmanueloluwatobi2000@gmail.com",
            "customer_mobile": "08156269921",
            "customer_address": "35, Abule Egun, Mowe, Ogun State",
            "items": [{"description": "Iphone 13 Pro Max Gold", "unit_price": "400000", "quantity": "1"}, {"description": "Samsung S22 Black", "unit_price": "550000", "quantity": "1"}],
            "currency": "NGN"
        }
        self.client.login(**self.user_data)
        resp = self.client.post(self.receipt_route, json.dumps(data), content_type='application/json')
        json_resp = resp.json()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(json_resp['status'], True)
        self.assertEqual(json_resp['error_code'], None)
    
    def test_get_receipts(self):
        self.client.login(**self.user_data)
        resp = self.client.get(self.receipt_route)
        self.assertEqual(resp.status_code, 200)
    
    def tearDown(self):
        super().tearDown()