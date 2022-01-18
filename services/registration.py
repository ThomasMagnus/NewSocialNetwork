import random
from random import choice
from werkzeug.security import generate_password_hash
from authorization.models import UserFile, ProFile
from django.contrib.auth.models import User
from .generate_id import generate_random_num


def registration(user_id, name, user_login, email, password):
    id_num = generate_random_num()
    user_hash_pass = generate_password_hash(password)
    user = UserFile(id=user_id, user_name=name, user_login=user_login, email=email,
                    password=user_hash_pass)
    user.save()

    return user

    # user_create = user.objects.create(username=user_login, password=user_hash_pass)
    # user_create.save()
