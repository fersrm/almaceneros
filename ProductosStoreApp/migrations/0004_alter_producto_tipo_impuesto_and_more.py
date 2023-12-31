# Generated by Django 4.2.4 on 2023-11-02 20:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "ProductosStoreApp",
            "0003_rename_nombre_producto_producto_descripcion_producto_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto",
            name="tipo_impuesto",
            field=models.IntegerField(choices=[(1, "IVA"), (2, "EXENTO")], default=1),
        ),
        migrations.AlterField(
            model_name="producto",
            name="tipo_medida",
            field=models.IntegerField(
                choices=[(1, "Unidad"), (2, "Granel")], default=1
            ),
        ),
    ]
