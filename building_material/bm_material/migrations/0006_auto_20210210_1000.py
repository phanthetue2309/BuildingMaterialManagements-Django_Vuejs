# Generated by Django 3.1.6 on 2021-02-10 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_material', '0005_auto_20210210_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailinputbill',
            name='price',
            field=models.IntegerField(default=10000),
        ),
    ]
