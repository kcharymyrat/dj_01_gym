from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product

from .models import Order
from .forms import OrderForm


@login_required
def order_checkout_view(request):
    product_id = request.session.get("product_id")
    if not product_id:
        return redirect("home")
    products_qs = Product.objects.filter(id=product_id)
    if not products_qs.exists():
        return redirect("home")
    product_obj = products_qs.first()

    order_id = request.session.get("order_id")
    if not order_id:
        order_obj = Order.objects.create(user=request.user, product=product_obj)
        request.session["order_id"] = order_obj.id
    else:
        order_qs = Order.objects.filter(id=order_id)
        if order_qs.exists():
            order_obj = Order.objects.get(id=order_id)
        else:
            del request.session["order_id"]
            return redirect("order_checkout")
    if order_obj.product.id != product_id:
        del request.session["order_id"]
        return redirect("order_checkout")

    form = OrderForm(request.POST or None, instance=order_obj)
    if form.is_valid():
        print(form.cleaned_data)
        shipping_address = form.cleaned_data.get("shipping_address")
        billing_address = form.cleaned_data.get("billing_address")
        order_obj.shipping_address = shipping_address
        order_obj.billing_address = billing_address
        order_obj.mark_paid()
        order_obj.update_inventory()
        order_obj.save()
        if product_obj.has_digital:
            request.session["downloadable_order_id"] = order_obj.id
            request.session["downloadable_product_id"] = order_obj.product.id
            print("downloadable_order_id", request.session["downloadable_order_id"])
            print("downloadable_product_id", request.session["downloadable_product_id"])
        del request.session["order_id"]
        del request.session["product_id"]
        return redirect("home")
    return render(
        request, "orders/order_checkout.html", {"form": form, "obj": order_obj}
    )


@login_required
def order_list_view(request, pk):
    orders = Order.objects.filter(user_id=pk)
    print(orders)
    return render(request, "orders/order_list.html", {"orders": orders})
