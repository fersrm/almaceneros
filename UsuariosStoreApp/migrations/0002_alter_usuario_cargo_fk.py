# Generated by Django 4.2.4 on 2023-11-16 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("UsuariosStoreApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="cargo_FK",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="UsuariosStoreApp.cargo",
            ),
        ),
    ]
