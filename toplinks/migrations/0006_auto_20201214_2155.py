# Generated by Django 3.1.4 on 2020-12-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toplinks', '0005_auto_20201214_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_user_name',
            field=models.CharField(max_length=110),
        ),
    ]
