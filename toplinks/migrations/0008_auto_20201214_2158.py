# Generated by Django 3.1.4 on 2020-12-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toplinks', '0007_auto_20201214_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='tweet_user_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tweet',
            name='tweet_user_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
