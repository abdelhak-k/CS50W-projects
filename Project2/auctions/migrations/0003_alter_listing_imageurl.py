# Generated by Django 5.0.7 on 2024-07-29 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_listing_user_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageUrl',
            field=models.ImageField(upload_to='listings/'),
        ),
    ]