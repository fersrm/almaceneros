from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.db import connection
from django_tenants.utils import get_public_schema_name
from ProductosStoreApp.models import Producto

# Create your models here.


class DatosEmpresa(models.Model):
    id_datos_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=45)
    rut_empresa = models.CharField(max_length=15)
    email = models.EmailField(max_length=64, default="pepe@gmail.com")
    telefono = models.CharField(max_length=15, default="123456789")
    comuna = models.CharField(max_length=45, default="Chillan")
    direccion_empresa = models.CharField(max_length=45)
    IVA = models.IntegerField()
    minimo_boleta = models.IntegerField(default=100)
    margen_global = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    def save(self, *args, **kwargs):
        try:
            original_instance = DatosEmpresa.objects.get(pk=1)
        except DatosEmpresa.DoesNotExist:
            original_instance = None

        if original_instance and self.margen_global != original_instance.margen_global:
            margen = self.margen_global

            productos = Producto.objects.all()
            for producto in productos:
                producto.precio_venta = float(
                    producto.precio_bruto_producto
                    * (1 + (margen + producto.margen_ganancia) / 100)
                )
                producto.precio_venta = round(producto.precio_venta)
                producto.save()

        super(DatosEmpresa, self).save(*args, **kwargs)

    class Meta:
        db_table = "datosempresa"

    def __str__(self):
        return f"{self.nombre_empresa}"


@receiver(post_migrate)
def create_default_datos_empresa(sender, **kwargs):
    tenant = connection.tenant
    if tenant and tenant.schema_name != get_public_schema_name():
        if sender.name == "DatosEmpresaStoreApp":
            DatosEmpresa.objects.get_or_create(
                id_datos_empresa=1,
                defaults={
                    "nombre_empresa": "Mi Empresa",
                    "rut_empresa": "12345678-9",
                    "email": "example@gmail.com",
                    "telefono": "+569123456",
                    "comuna": "Mi Comuna",
                    "direccion_empresa": "Mi Dirección",
                    "IVA": 19,
                    "minimo_boleta": 100,
                    "margen_global": 0,
                },
            )
