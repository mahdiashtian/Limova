from django.db import models

from core.models import BaseModel


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
    rate = models.IntegerField(verbose_name="امتیاز")

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
