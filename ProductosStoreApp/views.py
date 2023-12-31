# Librerías de Django
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from utils.custom_middleware import cargo_check
from django.contrib import messages
from django.shortcuts import redirect, render

# Modelos y formularios
from .forms import ProductoAgregarForm, ProductoEditarForm, PlusProductoForm
from .models import Producto
from django.db.models import F, Case, When, Value, IntegerField

# Para trabajar con clases
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

# imporat funciones
from utils.helpers import buscar_campos


# -----------------CRUD TIENDA-------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ProductoListView(ListView):
    model = Producto
    template_name = "tienda.html"
    paginate_by = 5

    def get_queryset(self):
        busqueda = self.request.GET.get("buscar")
        campos_busqueda = [
            "descripcion_producto",
            "codigo_producto",
            "stock",
            "categoria_FK__nombre_categoria",
        ]
        queryset = buscar_campos(self.model, campos_busqueda, busqueda)
        queryset = queryset.order_by("-id_producto")

        if not queryset and busqueda:
            messages.error(self.request, f"No Existe {busqueda}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        # -----------------------------------------------------------------------------      

        data = []

        for product in context["object_list"]:
            
            producto_id = product.id_producto
   
            query = Producto.objects.filter(id_producto__exact= producto_id)
            
            if query:
              descuento_promocion = Case(
                When(promociones__activo=True, then=F("promociones__descuento")),
                default=Value(0),
                output_field=IntegerField(),
              )

              query = query.annotate(descuento=descuento_promocion)

              if query.count() == 1:
                  query = query.annotate(descuento=descuento_promocion)

              elif query.count() > 1:
                  filtra_query = query.annotate(
                      descuento=descuento_promocion
                  ).filter(descuento__gt=0)

                  if filtra_query:
                      query = filtra_query
                

            query = query.first()
            data.append(query)

        context["object_list"] = data

        # ----------------------------------------------------------------------------
            
        paginator = Paginator(context["object_list"], self.paginate_by)
        page = self.request.GET.get("page")
        context["object_list"] = paginator.get_page(page)
        return context


# -------------------------------------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class AgregarProductoView(CreateView):
    model = Producto
    form_class = ProductoAgregarForm
    template_name = "modal/AddTienda.html"

    def form_valid(self, form):
        # Obtener el usuario logeado
        usuario_logeado = self.request.user
        # Asignar el usuario logeado al campo usuario_FK antes de guardar
        producto = form.save(commit=False)
        producto.usuario_FK = usuario_logeado
        producto.margen_ganancia = (
            producto.margen_ganancia - self.request.datos_empresa.margen_global
        )

        producto.save()
        messages.success(self.request, "Producto agregado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return HttpResponseRedirect("/tienda/")

    def get_success_url(self):
        return reverse_lazy("Tienda")


# --------------------------------------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class EditarProductoView(UpdateView):
    model = Producto
    form_class = ProductoEditarForm
    template_name = "modal/EditTienda.html"

    def form_valid(self, form):
        form.clean()
        producto = form.save(commit=False)
        producto.margen_ganancia = (
            producto.margen_ganancia - self.request.datos_empresa.margen_global
        )

        producto.save()
        messages.success(self.request, "Producto editado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return HttpResponseRedirect("/tienda/")

    def get_success_url(self):
        return reverse_lazy("Tienda")


# -------------------------------------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class EliminarProductoView(DeleteView):
    model = Producto
    success_url = reverse_lazy("Tienda")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Producto eliminado correctamente")
        self.object.delete()
        return redirect(self.get_success_url())


# -----------------------------------------------------


@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(cargo_check, name="dispatch")
class PlusProductoView(UpdateView):
    model = Producto
    form_class = PlusProductoForm
    template_name = "modal/PlusProduc.html"

    def form_valid(self, form):
        producto = form.instance
        stock_increment = form.cleaned_data.get("stock_increment")
        if stock_increment is not None:
            producto.stock += stock_increment
        form.save()
        messages.success(self.request, "Producto añadido correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return HttpResponseRedirect("/tienda/")

    def get_success_url(self):
        return reverse_lazy("Tienda")


# -----------------BAJO-STOCK-----------------------


@login_required(login_url="/login/")
def tabla_stock(request):
    # Acceder a los productos con stock bajo desde el contexto global
    productos_con_stock_bajo = request.productos_con_stock_bajo
    return render(
        request,
        "modal/TablaReponerStock.html",
        {"object_list": productos_con_stock_bajo},
    )
