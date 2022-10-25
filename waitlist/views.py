from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product

from .models import Waitlist
from .forms import WaitlistModelForm


def waitlist_form_view(request):
    form = WaitlistModelForm(request.POST or None)

    b_product_id = request.session.get("b_product_id")
    if not b_product_id:
        return redirect("home")
    if not Product.objects.filter(id=b_product_id).exists():
        del request.session["b_product_id"]
        return redirect("home")
    if not Product.objects.filter(id=b_product_id).first().can_backorder:
        del request.session["b_product_id"]
        return redirect("home")

    if form.is_valid():
        obj = form.save(commit=False)
        obj.product_id = b_product_id
        obj.save()
        form = WaitlistModelForm()
        return redirect("home")
    return render(request, "waitlist/waitlist_form.html", {"form": form})


@login_required
def waitlist_customer_view(request, pk):
    waitlist_qs = Waitlist.objects.filter(user_id=pk)
    print(waitlist_qs)
    return render(request, "waitlist/waitlist_customer.html", {"waitlist": waitlist_qs})
