# Generated by Django 4.2.4 on 2023-11-13 13:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ProductosStoreApp", "0007_alter_producto_stock"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto",
            name="stock",
            field=models.DecimalField(decimal_places=3, default=10.0, max_digits=10),
        ),
    ]