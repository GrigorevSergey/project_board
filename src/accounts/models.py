from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    DIVISION_CHOICES = [
        ("programmers", "Программисты"),
        ("testers", "Тестировщики"),
        ("designers", "Дизайнеры"),
        ("developers", "Разработчики"),
    ]

    POSITION_CHOICES = [
        ("tech_lead", "Тех_лид"),
        ("team_lead", "Тим_лид"),
        ("senior", "Сеньор"),
        ("middle", "Мидл"),
        ("junior", "Джун"),
    ]

    name = models.CharField(max_length=20, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True)
    division = models.CharField(
        max_length=20,
        choices=DIVISION_CHOICES,
        default="developers",
        verbose_name="Подразделение",
    )
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default="junior",
        verbose_name="Должность",
    )
    number_phone = models.CharField(
        max_length=20, unique=True, default="00000000000", verbose_name="Номер телефона"
    )
    notification = models.JSONField(
        default=dict, blank=True, null=True, verbose_name="Уведомление"
    )

    def __str__(self):
        return self.name
