# Generated by Django 3.2.7 on 2021-09-23 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_App', '0025_alter_contacts_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='phone',
            field=models.CharField(blank=True, default='+880', max_length=14, null=True),
        ),
    ]