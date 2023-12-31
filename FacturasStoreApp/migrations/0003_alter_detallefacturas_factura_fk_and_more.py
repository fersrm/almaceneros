# Generated by Django 4.2.4 on 2023-11-16 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ProductosStoreApp", "0008_alter_producto_stock"),
        ("FacturasStoreApp", "0002_alter_facturas_cliente_fk"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detallefacturas",
            name="factura_FK",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="FacturasStoreApp.facturas",
            ),
        ),
        migrations.AlterField(
            model_name="detallefacturas",
            name="producto_FK",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ProductosStoreApp.producto",
            ),
        ),
    ]
