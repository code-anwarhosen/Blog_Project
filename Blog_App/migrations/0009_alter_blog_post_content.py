# Generated by Django 3.2.7 on 2021-09-17 23:56

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_App', '0008_user_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_post',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]