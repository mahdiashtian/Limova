from django.db import models

from core.models import BaseModel


class ArticleModelManager(models.Manager):
    def get_next_and_previous(self, current_object):
        ordering = 'created_at'
        previous = self.filter(**{ordering + '__lt': current_object.created_at}).order_by('-created_at').first()
        next = self.filter(**{ordering + '__gt': current_object.created_at}).order_by('created_at').first()
        return previous, next


class Article(BaseModel):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    media = models.ForeignKey('core.Media', related_name='article', on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'archived_at__isnull': True}, verbose_name='رسانه')
    objects = ArticleModelManager()

    # tags = models.ManyToManyField('taxonomy.Tag', related_name='article',
    #                               limit_choices_to={'archived_at__isnull': True}, verbose_name='تگ ها')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'
