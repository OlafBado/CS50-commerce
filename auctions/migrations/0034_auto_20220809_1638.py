# Generated by Django 3.2.15 on 2022-08-09 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_auto_20220809_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auction'),
        ),
    ]