from django.db import models
from django.urls import reverse
from account.models import User
from django.utils.html import format_html
from django.utils import timezone
from extensions.utils import jalali_convertor

# Model Manager
class ArticelManager(models.Manager):
    def published(self):
        return self.filter(status='p')

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey(
        'self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='childre', verbose_name='زیر دسته'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name='پوزیشن')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),      # draft
        ('p', 'منتشر شده'),     # publish
        ('i', 'در حال بررسی'),  # investigation
        ('b', 'برگشت داده شده') # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name='نویسنده' )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته بندی')
    description = models.TextField( verbose_name='توضیحات')
    thumbnail = models.ImageField(upload_to='images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ارسال')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('account:home')

    def jpublish(self):
        return jalali_convertor(self.publish)
    jpublish.short_description = 'زمان انتشار'

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))

    def category_to_str(self):
        return '، '.join([category.title for category in self.category.active()])
    category_to_str.short_description = 'دسته بندی'

    thumbnail_tag.short_description = 'عکس'
    objects = ArticelManager()