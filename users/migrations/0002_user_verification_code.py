# Generated by Django 4.2.7 on 2023-12-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='код подтверждения почты'),
        ),
    ]
