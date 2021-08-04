from django.contrib.auth import authenticate
from authenticate.models import NewUser
import environ
import random
from rest_framework.exceptions import AuthenticationFailed

env = environ.Env()
environ.Env.read_env()

def generate_username(name):
    username = "".join(name.split(" ")).lower()
    if not NewUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 100))
        return generate_username(random_username)

def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = NewUser.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            register_user = authenticate(email=email, password=env("SOCIAL_SECRET"))
            return {
                "username": register_user.username,
                "email": register_user.email,
                "tokens": register_user.tokens()
            }

        else:
            raise AuthenticationFailed(detail="Please continue your login using" + filtered_user_by_email[0].auth_provider)
    else:
        user = {
            "username": generate_username(name),
            "email": email,
            "password": env("SOCIAL_SECRET"),
        }
        user = NewUser.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=env("SOCIAL_SECRET"))
        return {
            "email": new_user.email,
            "username": new_user.username,
            "tokens": new_user.tokens()
        }