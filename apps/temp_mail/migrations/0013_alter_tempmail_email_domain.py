# Generated by Django 4.1.4 on 2022-12-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_mail', '0012_alter_tempmail_temp_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempmail',
            name='email_domain',
            field=models.CharField(default='1secmail.com', max_length=255),
        ),
    ]