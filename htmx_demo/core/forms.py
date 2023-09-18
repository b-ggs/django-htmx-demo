from django import forms

from .models import Product


class AddToCartForm(forms.Form):
    template_name = "add-to-cart-form.html"

    quantity = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 4)])

    def __init__(self, product: Product, *args, **kwargs) -> None:
        self.product = product
        super().__init__(*args, **kwargs)

        if product.variants:
            self.fields["variant"] = forms.ChoiceField(
                choices=[(v, v) for v in product.variants]
            )
            self.fields["variant"].widget.attrs.update({"class": "input"})

        self.fields["quantity"].widget.attrs.update({"class": "input"})
