# Generated by Django 4.1.4 on 2022-12-26 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_mail', '0002_tempmail_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempmail',
            name='email_domain',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tempmail',
            name='email_username',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
