# Generated by Django 3.2.7 on 2021-09-18 00:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog_App', '0009_alter_blog_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]