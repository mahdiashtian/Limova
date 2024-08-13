from django.db import models

from core.models import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    media = models.ManyToManyField('core.Media', related_name='article',
                                   limit_choices_to={'archived_at__isnull': True}, verbose_name='رسانه')
    tags = models.ManyToManyField('taxonomy.Tag', related_name='article',
                                  limit_choices_to={'archived_at__isnull': True}, verbose_name='تگ ها')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'
