# Generated by Django 4.0.2 on 2022-02-09 18:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'مقاله', 'verbose_name_plural': 'مقالات'},
        ),
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.TimeField(auto_now_add=True, verbose_name='تاریخ ارسال'),
        ),
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='article',
            name='publish',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='تاریخ ارسال'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('d', 'پیش نویس'), ('p', 'منتشر شده')], max_length=1, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(upload_to='images', verbose_name='تصویر مقاله'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200, verbose_name='عنوان'),
        ),
    ]
