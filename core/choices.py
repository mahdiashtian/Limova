from django.db import models


class RuleChoices(models.TextChoices):
    DEVELOPER = "developer", "DEVELOPER"
    CEO = "ceo", "CEO"
    PR = "PR Manager", "PR Manager"
    MANAGING = "Managing Director", "Managing Director"
    HEAD = "Head of Stone Paper Engineering", "Head of Stone Paper Engineering"


class TypeChoices(models.TextChoices):
    PROFILE = "profile", "PROFILE"
    GALLERY = "gallery", "GALLERY"
    PRODUCT = "product", "PRODUCT"
    OTHER = "other", "OTHER"


class CommentTypeChoices(models.TextChoices):
    PRODUCT = "product", "PRODUCT"
    BLOG = "blog", "BLOG"
