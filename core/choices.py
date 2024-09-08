from django.db import models


class RuleChoices(models.TextChoices):
    DEVELOPER = "developer", "DEVELOPER"
    CEO = "ceo", "CEO"


class TypeChoices(models.TextChoices):
    PROFILE = "profile", "PROFILE"
    GALLERY = "gallery", "GALLERY"
    PRODUCT = "product", "PRODUCT"
    OTHER = "other", "OTHER"
