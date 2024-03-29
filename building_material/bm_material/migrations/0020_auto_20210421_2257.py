# Generated by Django 3.1.6 on 2021-04-21 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bm_material', '0019_product_calculationunit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopping',
            old_name='customer_account',
            new_name='staff',
        ),
        migrations.AddField(
            model_name='customer',
            name='discription',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='discription',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='inputbill',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='outputbill',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
