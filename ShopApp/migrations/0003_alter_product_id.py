# Generated by Django 4.2.2 on 2023-06-29 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0002_rename_payment_date_payment_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
