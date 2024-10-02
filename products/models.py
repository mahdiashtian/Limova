from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, Media

User = get_user_model()


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
    # sizes = models.ManyToManyField(ProductSize, related_name='products', verbose_name="سایز ها", blank=True)
    images = models.ManyToManyField(Media, related_name='products', verbose_name="تصاویر", blank=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصول ها'


class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', _('در انتظار')),
        ('paid', _('پرداخت شده')),
        ('shipped', _('ارسال شده')),
        ('delivered', _('تحویل داده شده')),
        ('canceled', _('لغو شده')),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت سفارش")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="مجموع مبلغ", default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="تخفیف", default=0)
    payment_reference = models.CharField(max_length=100, null=True, blank=True, verbose_name="کد پرداخت")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ کل", default=0)

    def save(self, *args, **kwargs):
        # Use Django's aggregation to sum price * quantity and discount * quantity
        if not self.pk:
            return super().save(*args, **kwargs)
        else:
            totals = self.items.aggregate(
                total_amount=Sum(F('price') * F('quantity')),
                total_discount=Sum(F('discount') * F('quantity'))
            )

            # Assign the aggregated values to total_amount and total_discount
            self.total_amount = totals['total_amount'] or 0  # Handle None by assigning 0
            self.total_discount = totals['total_discount'] or 0  # Handle None by assigning 0
            self.total_price = self.total_amount - self.total_discount
            # Now save the order
            return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"

    def __str__(self):
        return f"Order #{self.id} - {self.owner}"


class OrderItem(BaseModel):
    owner = None
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="محصول")
    quantity = models.PositiveIntegerField(verbose_name="تعداد", default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت واحد")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="تخفیف", default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت نهایی", default=0)

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        discount = self.product.discount
        self.price = self.product.price
        if discount and discount.is_active:
            self.discount = self.price * discount.value / 100
        self.final_price = (self.price - self.discount) * self.quantity
        instance = super().save()
        self.order.save()
        return instance

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
