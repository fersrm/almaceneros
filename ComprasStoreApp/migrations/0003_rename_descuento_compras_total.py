# Generated by Django 4.2.4 on 2023-11-13 14:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ComprasStoreApp", "0002_alter_compras_tipo_impuesto"),
    ]

    operations = [
        migrations.RenameField(
            model_name="compras",
            old_name="descuento",
            new_name="total",
        ),
    ]
