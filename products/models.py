from django.db import models
from django.utils import timezone

from core.models import BaseModel, Media


class ProductDiscount(models.Model):
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    value = models.PositiveSmallIntegerField(verbose_name="درصد", default=0)

    @property
    def is_active(self):
        print(True if timezone.now() > self.end_date else False)
        return True if self.start_date < timezone.now() < self.end_date else False

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'


class ProductColor(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'


class ProductSize(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'


class Product(BaseModel):
    name = models.CharField(max_length=50, verbose_name="نام")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    description = models.TextField(verbose_name="توضیحات")
    availability = models.PositiveSmallIntegerField(verbose_name="تعداد کالای باقی مانده")
    discount = models.ForeignKey(ProductDiscount, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name="تخفیف")
    tags = models.ManyToManyField('taxonomy.Tag', related_name='products', verbose_name="تگ ها", blank=True)
    categories = models.ManyToManyField('taxonomy.Category', related_name='products', verbose_name="دسته بندی ها",
                                        blank=True)
    colors = models.ManyToManyField(ProductColor, related_name='products', verbose_name="رنگ ها", blank=True)
    sizes = models.ManyToManyField(ProductSize, related_name='products', verbose_name="سایز ها", blank=True)
    images = models.ManyToManyField(Media, related_name='products', verbose_name="تصاویر", blank=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصول ها'
