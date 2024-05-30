from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import UAV, Rental
from datetime import datetime, timedelta
from django.test.utils import override_settings
from .factories import UserFactory, UAVFactory, RentalFactory

class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 't@t.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
    
    def user_login(self):
        url = reverse('login')
        data = {
            'username': self.user.username,
            'password': 'password123'
        }
        return self.client.post(url, data, format='json')

    def test_user_login(self):
        response = self.user_login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_user_login_wrong_password(self):
        url = reverse('login')
        data = {
            'username': self.user.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
    
    def test_user_refresh(self):
        response = self.user_login()
        url = reverse('refresh')
        data = {
            'refresh': response.data['refresh']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_refresh_wrong_token(self):
        response = self.user_login()
        url = reverse('refresh')
        data = {
            'refresh': 'wrongtoken'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)

class UAVTests(APITestCase):
    def setUp(self):
        self.create_user_and_get_token()
        self.create_uav_instance()

    def create_user_and_get_token(self):
        self.user = UserFactory()
        self.client.login(username=self.user.username, password='password123')
        url = reverse('login')
        response = self.client.post(url, {'username': self.user.username, 'password': 'password123'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def create_uav_instance(self):
        self.uav = UAVFactory()
        self.uav_url = reverse('uav-detail', args=[self.uav.id])
        self.uav1 = UAV.objects.create(brand="DJI", model="Phantom", weight=1.2, category="Quadcopter")
        self.uav2 = UAV.objects.create(brand="Parrot", model="Anafi", weight=0.8, category="Quadcopter")
        self.uav3 = UAV.objects.create(brand="DJI", model="Mavic", weight=1.5, category="Quadcopter")

    def test_create_uav(self):
        response = self.create_uav()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UAV.objects.count(), 5)

    def test_list_uavs(self):
        response = self.list_uavs()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 4)

    def test_retrieve_uav(self):
        response = self.retrieve_uav()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], self.uav.brand)

    def test_update_uav(self):
        response = self.update_uav()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.uav.refresh_from_db()
        self.assertEqual(self.uav.model, 'Phantom 4 Pro')

    def test_delete_uav(self):
        response = self.delete_uav()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UAV.objects.count(), 3)

    def create_uav(self):
        url = reverse('uav-list-create')
        data = {
            'brand': 'Parrot',
            'model': 'Anafi',
            'weight': 0.32,
            'category': 'Quadcopter'
        }
        return self.client.post(url, data, format='json')

    def list_uavs(self):
        url = reverse('uav-list-create')
        return self.client.get(url, format='json')

    def retrieve_uav(self):
        return self.client.get(self.uav_url, format='json')

    def update_uav(self):
        data = {
            'brand': 'DJI',
            'model': 'Phantom 4 Pro',
            'weight': 1.38,
            'category': 'Quadcopter'
        }
        return self.client.put(self.uav_url, data, format='json')

    def delete_uav(self):
        return self.client.delete(self.uav_url)
    
    def test_filter_by_brand(self):
        self.delete_uav()
        response = self.client.get(reverse('uav-list-create'), {'brand': 'DJI'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['brand'], 'DJI')
        self.assertEqual(response.data['data'][1]['brand'], 'DJI')

    def test_filter_by_weight_gte(self):
        self.delete_uav()
        response = self.client.get(reverse('uav-list-create'), {'weight__gte': 1.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['weight'], 1.2)
        self.assertEqual(response.data['data'][1]['weight'], 1.5)
    
    def test_search_by_model(self):
        self.delete_uav()
        response = self.client.get(reverse('uav-list-create'), {'search': 'Phantom'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['model'], 'Phantom')
    
    def test_order_by_model(self):
        self.delete_uav()
        response = self.client.get(reverse('uav-list-create'), {'ordering': 'model'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['model'], 'Anafi')

@override_settings(USE_TZ = False)
class RentalTests(APITestCase):
    def setUp(self):
        self.create_user_and_get_token()
        self.create_uav_instance()
        self.create_rental_instance()
        
    def create_user_and_get_token(self):
        self.user = UserFactory()
        self.client.login(username=self.user.username, password='password123')
        url = reverse('login')
        response = self.client.post(url, {'username': self.user.username, 'password': 'password123'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def create_uav_instance(self):
        self.uav = UAVFactory()

    def create_rental_instance(self):
        self.rental = RentalFactory(renting_member=self.user, uav=self.uav)
        self.rental_url = reverse('rental-detail', args=[self.rental.id])
    
    def test_rent_uav(self):
        url = reverse('uav-rent', args=[self.uav.id])
        data = {
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=1)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rental.objects.count(), 2)

    def test_list_rentals(self):
        response = self.list_rentals()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_retrieve_rental(self):
        response = self.retrieve_rental()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uav']['id'], self.rental.uav.id)

    def test_update_rental(self):
        new_end_date = datetime.now() + timedelta(days=2)
        response = self.update_rental(new_end_date)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.rental.refresh_from_db()
        self.assertEqual(self.rental.end_date, new_end_date)

    def test_delete_rental(self):
        response = self.delete_rental()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rental.objects.count(), 0)

    def list_rentals(self):
        url = reverse('rental-list')
        return self.client.get(url, format='json')

    def retrieve_rental(self):
        return self.client.get(self.rental_url, format='json')

    def update_rental(self, new_end_date):
        data = {
            'uav_id': self.uav.id,
            'renting_member_id': self.user.id,
            'start_date': self.rental.start_date.isoformat(),
            'end_date': new_end_date.isoformat()
        }
        return self.client.put(self.rental_url, data, format='json')

    def delete_rental(self):
        return self.client.delete(self.rental_url)