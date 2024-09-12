from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from articles.models import Article
from core.choices import CommentTypeChoices
from core.models import BaseModel
from products.models import Product


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Comment(BaseModel):
    text = models.CharField(max_length=255, verbose_name="متن کامنت")
    rate = models.IntegerField(verbose_name="امتیاز", validators=[MinValueValidator(0), MaxValueValidator(5)])
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    type = models.CharField(choices=CommentTypeChoices.choices, default=CommentTypeChoices.PRODUCT)

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        if self.type == CommentTypeChoices.PRODUCT:
            self.content_type = ContentType.objects.get_for_model(Product)
        elif self.type == CommentTypeChoices.BLOG:
            self.content_type = ContentType.objects.get_for_model(Article)
        return super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        indexes = [
            models.Index(fields=["content_type", "object_id", "type"]),
        ]
