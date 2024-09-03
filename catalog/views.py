from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "products_list.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"You have new message from {name}({phone}): {message}")
    return render(request, "contact.html")


def product_about(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_about.html', context)
