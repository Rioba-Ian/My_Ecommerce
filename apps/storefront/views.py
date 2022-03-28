from django.shortcuts import render, redirect

from apps.product.models import Product
from .forms import ContactForm

# Create your views here.
def frontpage(request):
    newest_products = Product.objects.all()
    return render(request,"storefront/frontpage.html",{'newest_products':newest_products})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')

        
    form = ContactForm()
    context = {'form':form}
    return render(request,"storefront/contact.html", context)

def success(request):
    return render(request, 'storefront/success.html')