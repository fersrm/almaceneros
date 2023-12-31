from django.db import models
from .choices import tipoMedida, tipoImpuesto
from django.db import connection
from django_tenants.utils import get_public_schema_name
from UsuariosStoreApp.models import Usuario

# son para borrar imagen al actualizar
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_migrate

# Create your models here.


def dynamic_upload_path(instance, filename):
    return "productos/{}".format(filename)


# -----------------------Productos----------------


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=45, unique=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            last_instance = Categoria.objects.order_by("-id_categoria").first()

            if last_instance.id_categoria:
                self.id_categoria = last_instance.id_categoria + 1

        super(Categoria, self).save(*args, **kwargs)

    class Meta:
        db_table = "categoria"

    def __str__(self):
        return f"{self.nombre_categoria}"


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=45, unique=True)
    descripcion_producto = models.CharField(max_length=45)
    precio_bruto_producto = models.IntegerField()
    precio_venta = models.IntegerField(default=10)
    margen_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    imagen = models.ImageField(
        upload_to=dynamic_upload_path, null=True, blank=True, default=None
    )
    stock = models.DecimalField(max_digits=10, decimal_places=3, default=10.000)
    fecha = models.DateField(auto_now_add=True)
    tipo_medida = models.IntegerField(choices=tipoMedida, default=1)
    tipo_impuesto = models.IntegerField(choices=tipoImpuesto, default=1)
    usuario_FK = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    categoria_FK = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "producto"

    def __str__(self):
        return f"{self.descripcion_producto}"

    def borrar_imagen_anterior(self):
        if self.id_producto is not None and self.imagen:
            try:
                producto_anterior = Producto.objects.get(id_producto=self.id_producto)
                if producto_anterior.imagen and producto_anterior.imagen != self.imagen:
                    ruta_img = os.path.abspath(producto_anterior.imagen.path)
                    if os.path.exists(ruta_img):
                        os.remove(ruta_img)
            except Producto.DoesNotExist as e:
                print(f"Producto con id {self.id_producto} no funciona: {e}")


@receiver(pre_save, sender=Producto)
def borrar_imagen_anterior(sender, instance, **kwargs):
    instance.borrar_imagen_anterior()


@receiver(post_migrate)
def create_default_categorias(sender, **kwargs):
    tenant = connection.tenant
    if tenant and tenant.schema_name != get_public_schema_name():
        if sender.name == "ProductosStoreApp":
            Categoria.objects.get_or_create(
                id_categoria=1, defaults={"nombre_categoria": "VIVERES"}
            )
            Categoria.objects.get_or_create(
                id_categoria=2, defaults={"nombre_categoria": "BEBIDAS"}
            )
            Categoria.objects.get_or_create(
                id_categoria=3, defaults={"nombre_categoria": "CONDIMENTOS"}
            )
            Categoria.objects.get_or_create(
                id_categoria=4, defaults={"nombre_categoria": "VEGETALES"}
            )
