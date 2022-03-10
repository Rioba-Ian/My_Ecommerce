from django.shortcuts import render

from apps.product.models import Product

# Create your views here.
def frontpage(request):
    newest_products = Product.objects.all()
    return render(request,"storefront/frontpage.html",{'newest_products':newest_products})

def contact(request):
    return render(request,"storefront/contact.html")
