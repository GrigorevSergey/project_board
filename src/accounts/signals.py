# signals.py
from django.dispatch import Signal, receiver

user_registered = Signal()


@receiver(user_registered)
def handle_user_registration(sender, **kwargs):
    user = kwargs["user"]
    print(f"Новый пользователь зарегистрирован: {user.number_phone}")
