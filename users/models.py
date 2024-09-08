from django.contrib.auth.models import AbstractUser
from django.db import models

from core.choices import RuleChoices


class User(AbstractUser):
    avatar = models.ForeignKey('core.Media', null=True, blank=True, verbose_name="تصویر پروفایل",
                               on_delete=models.SET_NULL)
    rule = models.CharField(max_length=50, choices=RuleChoices.choices, default=RuleChoices.DEVELOPER)
