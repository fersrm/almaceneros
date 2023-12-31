from django.contrib import admin
from PromocionesStoreApp.models import Promociones

# Clase base de administración con el método común


class SharedModelAdminBase(admin.ModelAdmin):
    def has_module_permission(self, request):
        tenant_type = request.tenant.type
        allowed_tenant_types = ["type1", "type2"]
        return tenant_type in allowed_tenant_types


@admin.register(Promociones)
class PromocionesAdmin(SharedModelAdminBase):
    list_display = ("id_promocion", "descuento", "producto_FK", "activo")
