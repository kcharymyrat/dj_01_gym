from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from pathlib import Path
from mimetypes import guess_type
from wsgiref.util import FileWrapper

from orders.models import Order

from .models import Product
from .forms import ProductModelForm


def home_view(request, *args, **kwargs):
    q = request.GET.get("q")
    if q:
        qs = Product.objects.filter(is_featured=True).filter(title__icontains=q)
    else:
        qs = Product.objects.filter(is_featured=True) | Product.objects.filter(
            can_backorder=True
        )
    context = {"products": qs}
    return render(request, "products/index.html", context)


def product_details_view(request, pk, *args, **kwargs):
    product = Product.objects.filter(pk=pk).first()
    print(product.title)
    if request.POST:
        if not product.has_invetory() and product.can_backorder:
            request.session["b_product_id"] = product.id
            return redirect("waitlist_form")
        request.session["product_id"] = product.id
        return redirect("checkout")
    print(request.session.get("product_id"))
    return render(request, "products/product_details.html", {"product": product})


@staff_member_required
def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None, request.FILES or None)
    print(request.FILES)
    if form.is_valid():
        print("form =", form.cleaned_data)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.image = request.FILES.get("image")
        obj.file = request.FILES.get("file")
        obj.save()
        form = ProductModelForm()
    return render(request, "products/product_create.html", {"form": form})


@login_required
def download_view(request):
    order_id = request.session.get("downloadable_order_id")
    product_id = request.session.get("downloadable_product_id")
    if not order_id or not product_id:
        return redirect("home")
    order_obj = Order.objects.filter(id=order_id).first()
    if order_obj.product.id != product_id:
        return redirect("home")

    qs = Product.objects.filter(file__isnull=False).filter(id=product_id)
    print("qs =", qs)
    product = qs.first()

    file_path = product.file.path
    path = Path(file_path)
    if not path.exists():
        raise Http404
    ext = path.suffix
    file_name = f"{product.title}-{order_id}{ext}"
    with open(path, "rb") as file:
        wrapper = FileWrapper(file)
        content_type = "application/force-download"
        guessed_ = guess_type(path)[0]
        if guessed_:
            content_type = guessed_
        response = HttpResponse(wrapper, content_type=content_type)
        response["Content-Disposition"] = f"attachement; filename={file_name}"
        response["X-SendFile"] = f"{file_name}"
        return response
