# Generated by Django 4.0.3 on 2022-12-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0005_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_address',
            name='phone_no',
            field=models.TextField(default='9999888822'),
            preserve_default=False,
        ),
    ]
