import datetime
import random
from datetime import timedelta

from api import models
from faker import Faker
import phonenumbers


def format_phone(phone: str):
    return phonenumbers.format_number(phonenumbers.parse(phone, 'RU'), phonenumbers.PhoneNumberFormat.E164)


def create_random_clients():
    count = 54

    faker = Faker(["ru_RU"])

    global_password = '12345678'

    for _ in range(count):
        rand_username = format_phone(faker.phone_number())
        first_name = faker.first_name()
        last_name = faker.last_name()
        models.User.objects.create_user(
            username=rand_username,
            password=global_password,
            first_name=first_name,
            last_name=last_name
        )


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def fill_commercial_rooms():
    commercial_types = list(models.Commercial.objects.all())
    client_list = list(models.Client.objects.all())
    statuses = ("Продано", "Арендуется")

    for room in models.Room.objects.all():
        rand_val = random.random()

        # 60% комнат будет куплено/арендовано
        if rand_val > 0.4:
            rand_client = random.choice(client_list)
            commercial_type = random.choice(commercial_types)
            status = random.choice(statuses)
            date = random_date(datetime.datetime(2021, 1, 1), datetime.datetime(2022, 1, 1)).date()
            price_per_month = None
            if status == "Арендуется":
                price_per_month = random.randint(65, 135) * 1000

            models.ClientRoom.objects.create(room=room,
                                             client=rand_client,
                                             commercial_type=commercial_type,
                                             status=status,
                                             price_per_month=price_per_month,
                                             created_at=date)
