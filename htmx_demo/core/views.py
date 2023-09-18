from django.db.models import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin, View

from .forms import AddToCartForm
from .models import CartItem, Product


class BaseView(ContextMixin, View):
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            return context

        context["cart_item_count"] = CartItem.objects.filter(
            user=self.request.user
        ).count()

        return context


class IndexView(TemplateView, BaseView):
    template_name = "index.html"


class AboutView(TemplateView, BaseView):
    template_name = "about.html"


class ProductListView(ListView, BaseView):
    model = Product
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Product]:
        if self.should_render_static_page():
            return Product.objects.none()
        return super().get_queryset()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        if self.should_render_static_page():
            return context

        context["object_rows"] = [
            context["object_list"][i : i + 3]
            for i in range(0, len(context["object_list"]), 3)
        ]

        return context

    def get_template_names(self) -> list[str]:
        if self.should_render_static_page():
            return ["product-list.html"]
        return ["product-list-infinite-scroll-page.html"]

    def should_render_static_page(self) -> bool:
        return (
            "Hx-Boosted" in self.request.headers
            or "Hx-Request" not in self.request.headers
        )


class ProductDetailView(DetailView, BaseView):
    template_name = "product-detail.html"
    model = Product


class AddToCartView(TemplateView, BaseView):
    template_name = "add-to-cart.html"

    def setup(self, *args, product_pk: int, **kwargs) -> None:
        self.product = get_object_or_404(Product, pk=product_pk)
        super().setup(*args, **kwargs)

    def post(self, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict:
        if not self.request.user.is_authenticated:
            return super().get_context_data(**kwargs)

        add_to_cart_success = False

        if self.request.method == "POST":
            form = AddToCartForm(self.product, self.request.POST)
            if form.is_valid():
                quantity = int(form.cleaned_data["quantity"])
                variant = form.cleaned_data.get("variant", "")

                CartItem.objects.create(
                    user=self.request.user,
                    product=self.product,
                    quantity=quantity,
                    variant=variant,
                )

                add_to_cart_success = True
        else:
            form = AddToCartForm(self.product)

        context = super().get_context_data(**kwargs)

        context["form"] = form
        context["product_pk"] = self.product.pk
        context["add_to_cart_success"] = add_to_cart_success

        return context


class CartView(TemplateView, BaseView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        context["cart_items"] = CartItem.objects.filter(
            user=self.request.user
        ).select_related("product")

        return context


class CartDeleteView(TemplateView, BaseView):
    template_name = "cart-delete.html"

    def setup(self, *args, cart_item_pk: int, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.cart_item = get_object_or_404(
            CartItem, pk=cart_item_pk, user=self.request.user
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        self.cart_item.delete()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        return context
