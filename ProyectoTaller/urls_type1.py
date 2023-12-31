from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("SistemaStoreApp.urls")),
    path("tienda/", include("ProductosStoreApp.urls")),
    path("usuarios/", include("UsuariosStoreApp.urls")),
    path("setting/", include("DatosEmpresaStoreApp.urls")),
    path("ventas/", include("VentasStoreApp.urls")),
    path("proveedores/", include("ProveedoresStoreApp.urls")),
    path("compras/", include("ComprasStoreApp.urls")),
    path("perfil/", include("PerfilStoreApp.urls")),
    path("promociones/", include("PromocionesStoreApp.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
