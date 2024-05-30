# factory design pattern for seeder and unit test

import factory
from django.contrib.auth.models import User
from rest_api.models import UAV, Rental
from faker import Faker
from datetime import timedelta

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class UAVFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UAV

    brand = factory.Faker('company')
    model = factory.Faker('word')
    weight = factory.LazyAttribute(lambda x: round(fake.random_number(digits=3) / 100, 2))
    category = factory.Faker('word')

class RentalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rental

    uav = factory.SubFactory(UAVFactory)
    renting_member = factory.SubFactory(UserFactory)
    start_date = factory.Faker('date_time_this_year')
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=1))
