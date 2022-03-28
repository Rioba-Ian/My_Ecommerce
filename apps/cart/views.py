from django.conf import settings
from django.contrib import messages 

from django.shortcuts import render, redirect

from apps.product.models import Product, updateStock
from apps.order.models import OrderItem
from .cart import Cart
from .forms import CheckoutForm
from apps.order.utilities import checkout


# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']

            order = checkout(request, first_name, last_name, email, city, street, phone)

            cart.clear()

            order.save()

            order_items = order.products.all()
            for item in order_items:
                item.product.stock -= item.quantity
                item.save()
                item.product.save()

            order.save()

            return redirect('success')
    
    else:
        form = CheckoutForm()


    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity','')
    quantity = request.GET.get('quantity','')

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')

    return render(request, 'cart/cart.html', {'form':form})

def success(request):
    return render(request, 'cart/success.html')


def reduce_stock(request, pk):
    product = Product.objects.get(id=pk)
    form = updateStock(request.POST)

    if request.method == "POST":
        if form.is_valid():
            quantity = int(request.POST['stock'])
            product.stock -= quantity
            product.save()
            return redirect('frontpage')

    return render(request, 'cart/success.html',{'form':form})