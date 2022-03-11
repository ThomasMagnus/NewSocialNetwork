from werkzeug.security import generate_password_hash
from authorization.models import UserFile


def registration(user_id, name, user_login, email, password):
    user_hash_pass = generate_password_hash(password)
    user = UserFile(id=user_id, user_name=name, user_login=user_login, email=email,
                    password=user_hash_pass)
    user.save()

    return user
