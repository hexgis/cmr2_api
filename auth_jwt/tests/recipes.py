from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from model_mommy.recipe import Recipe


class Recipes:

    def __init__(self):
        self.user = Recipe(
            User,
            username='user',
            password=make_password('top_secret')
        )
