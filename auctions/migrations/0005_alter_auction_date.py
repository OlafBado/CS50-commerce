# Generated by Django 3.2.15 on 2022-08-07 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
