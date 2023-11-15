# Generated by Django 4.2.4 on 2023-11-14 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("VentasStoreApp", "0001_initial"),
        (
            "ClientesStoreApp",
            "0002_remove_cliente_comuna_fk_remove_cliente_razon_social_and_more",
        ),
        ("ProductosStoreApp", "0008_alter_producto_stock"),
    ]

    operations = [
        migrations.CreateModel(
            name="Facturas",
            fields=[
                ("id_factura", models.AutoField(primary_key=True, serialize=False)),
                ("total_factura", models.IntegerField()),
                (
                    "cliente_fk",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ClientesStoreApp.cliente",
                    ),
                ),
                (
                    "venta_FK",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="VentasStoreApp.ventas",
                    ),
                ),
            ],
            options={
                "db_table": "facturas",
            },
        ),
        migrations.CreateModel(
            name="DetalleFacturas",
            fields=[
                (
                    "id_detalle_factura",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("cantidad", models.IntegerField()),
                ("total", models.IntegerField()),
                (
                    "factura_FK",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="FacturasStoreApp.facturas",
                    ),
                ),
                (
                    "producto_FK",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ProductosStoreApp.producto",
                    ),
                ),
            ],
            options={
                "db_table": "detallefactura",
            },
        ),
    ]