from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class BaseModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='سازنده')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ اپدیت')
    archived_at = models.DateTimeField(null=True, blank=True, editable=False, verbose_name='تاریخ حذف')

    class Meta:
        abstract = True


class Media(BaseModel):
    owner = None
    media = models.FileField()

    class Meta:
        verbose_name = 'رسانه'
        verbose_name_plural = 'رسانه ها'


class ContactUs(BaseModel):
    owner = None
    name = models.CharField(max_length=90)
    email = models.EmailField()
    subject = models.CharField(max_length=60)
    message = models.TextField()
