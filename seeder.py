import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uav_rental.settings')
django.setup()

from rest_api.factories import UserFactory, UAVFactory, RentalFactory
from django.test.utils import override_settings
from faker import Faker

fake = Faker()

def seed_users(n):
    users = [UserFactory() for _ in range(n)]
    return users

def seed_uavs(n):
    uavs = [UAVFactory() for _ in range(n)]
    return uavs

@override_settings(USE_TZ = False)
def seed_rentals(users, uavs, n):
    for _ in range(n):
        RentalFactory(renting_member=fake.random_element(users), uav=fake.random_element(uavs))

if __name__ == '__main__':
    print("creating fake data...")
    users = seed_users(5)
    uavs = seed_uavs(20)
    seed_rentals(users, uavs, 1000)
    print("fake data created.")
