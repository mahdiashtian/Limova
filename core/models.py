from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.choices import TypeChoices

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
    type = models.CharField(max_length=30, choices=TypeChoices.choices, default=TypeChoices.OTHER)
    name = models.CharField(null=True, blank=True, max_length=50)

    class Meta:
        verbose_name = 'رسانه'
        verbose_name_plural = 'رسانه ها'

    def __str__(self):
        return f"{self.id}-{self.type}-{self.name}"


class ContactUs(BaseModel):
    owner = None
    name = models.CharField(max_length=90, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    subject = models.CharField(max_length=60, verbose_name='موضوع')
    message = models.TextField(verbose_name='متن پیام')

    class Meta:
        verbose_name = 'تماس'
        verbose_name_plural = 'تماس ها'


class AboutUs(BaseModel):
    owner = None
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, verbose_name="تصویر", related_name='about_us_image',
                              null=True, blank=True)
    title_1 = models.CharField(max_length=255, verbose_name="عنوان یک")
    under_title_1 = models.TextField(verbose_name="زیر عنوان یک")
    title_2 = models.CharField(max_length=255, verbose_name="عنوان دو")
    under_title_2 = models.TextField(verbose_name="زیر عنوان دو")
    title_3 = models.CharField(max_length=255, verbose_name="عنوان سه")
    under_title_3 = models.TextField(verbose_name="زیر عنوان سه")
    gallery = models.ManyToManyField(Media, related_name='about_us_gallery', blank=True)

    # def clean(self):
    #     super().clean()
    #     photo = self.image.media
    #     if photo:
    #         img = Image.open(photo)
    #         width, height = img.size
    #         if width < 566 or height < 478:
    #             raise ValidationError(f"Image must be at least 566x478 pixels. Current size: {width}x{height}.")

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     thumbnail = self.thumbnail
    #     if thumbnail:
    #         thumbnail_media = thumbnail.media
    #         if os.path.isfile(thumbnail_media.path):
    #             os.remove(thumbnail_media.path)
    #     self.thumbnail = Media.objects.create(media=create_thumbnail(self.image.media), type=TypeChoices.THUMBNAIL)
    #
    #     super().save(*args, **kwargs)
    #     if thumbnail:
    #         thumbnail.delete()

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'


class Slider(BaseModel):
    owner = None
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    small_text = models.CharField(max_length=25)
    medium_text = models.CharField(max_length=50)
    large_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'


class Feature(BaseModel):
    owner = None
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"


class Meet(BaseModel):
    owner = None
    email = models.EmailField()
    count = models.PositiveSmallIntegerField()
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    message = models.TextField()

    class Meta:
        verbose_name = "ملاقات"
        verbose_name_plural = "ملاقات ها"


class WorkTime(BaseModel):
    owner = None
    name = models.CharField(max_length=50, verbose_name="نام روز هفته")
    start = models.TimeField(verbose_name="ساعت شروع")
    end = models.TimeField(verbose_name="ساعت پایان")
    close = models.BooleanField(default=False, verbose_name="بسته است", null=True, blank=True)

    @property
    def formatted_time_range(self):
        if self.close:
            return f'<li><span class="day">{self.name}</span><span class="time">Closed</span></li>'
        start_time_str = self.start.strftime('%I.%M%p').lower().lstrip('0')
        end_time_str = self.end.strftime('%I.%M%p').lower().lstrip('0')
        return f'<li><span class="day">{self.name}</span><span class="time">{start_time_str} - {end_time_str}</span></li>'

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         return super(*args, **kwargs)
    #     elif not self.start or not self.end:
    #         self.close = True
    #     else:
    #         self.close = False
    #     return super(*args, **kwargs)

    class Meta:
        verbose_name = "ساعت کاری"
        verbose_name_plural = "ساعت های کاری"
