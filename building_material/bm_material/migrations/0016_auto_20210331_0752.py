# Generated by Django 3.1.6 on 2021-03-31 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_material', '0015_shopping_buying_unit_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.IntegerField(default=10000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_cost',
            field=models.IntegerField(default=10000),
        ),
    ]