from djongo import models
from django.utils import timezone
from extensions.utils import jalali_converter

# my managers


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status='y')


# Create your models here.


class Category(models.Model):
    STATUS_CHOICES = (
        ('y', 'بله'),
        ('n', 'خیر'),
    )
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیر دست')
    title = models.CharField(max_length=255, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='تگ')
    # stat = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    status = models.CharField(default='y', max_length=1, choices=STATUS_CHOICES, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['-status', 'parent__id', '-position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویش'),
        ('p', 'منتشر شده'),
    )
    title = models.CharField(max_length=255, verbose_name='موضوع')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='تگ')
    category = models.ManyToManyField(Category, verbose_name="دسته بندی", related_name="articles")
    description = models.TextField(verbose_name='محتوا')
    image = models.ImageField(upload_to="images", verbose_name='عکس')
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='نوشته شده در تاریخ')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def jalali_publish(self):
        return jalali_converter(self.publish)
    jalali_publish.short_description = "زمان انتشار"

    def category_published(self):
        return self.category.filter(status="y")

    objects = ArticleManager()




