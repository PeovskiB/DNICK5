from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Product, Cart, Payment, CartItem

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'create_product.html'
    fields = '__all__'
    success_url = reverse_lazy('product_list')


class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class PaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = 'payment.html'
    fields = ['total_amount']
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Create a non-admin user
        user = User.objects.create_user(username=username, password=password)

        # Log in the user
        login(request, user)

        # Redirect to a specific page or the homepage
        return redirect('product_list')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product_details.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the user already has a cart
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            # Create a new cart for the user
            cart = Cart.objects.create(user=request.user)
    else:
        # If the user is not authenticated, use a session-based cart
        cart_id = request.session.get('cart_id')
        if not cart_id:
            # Create a new cart and store the cart ID in the session
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        else:
            # Retrieve the existing cart from the session
            cart = Cart.objects.filter(id=cart_id).first()
            if not cart:
                # Create a new cart if the existing cart is not found
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id

    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.quantity:
        # Redirect with a message indicating that the product is out of stock
        return redirect('out_of_stock')

    # Add the product to the cart or update its quantity
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    product.quantity -= quantity
    product.save()

    return redirect('product_details', product_id=product_id)


def out_of_stock(request):
    return render(request, 'out_of_stock.html')


class ProductDeleteView(View):
    def post(self, request, product_id):
        # Retrieve the product to be deleted
        product = get_object_or_404(Product, id=product_id)

        # Delete the product and remove its image file
        product.image.delete()
        product.delete()

        # Redirect to the product list page
        return redirect('product_list')


def payment(request):
    if request.method == 'POST':
        # Process the payment form submission
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Retrieve the user's cart
        cart = Cart.objects.get(user=request.user)

        # Calculate the total amount
        total_amount = 0
        cart_items = cart.cartitem_set.all()
        for cart_item in cart_items:
            total_amount += cart_item.product.price * cart_item.quantity

        # Create a payment instance
        payment = Payment.objects.create(user=request.user, total_amount=total_amount)

        # Update the cart items and product quantities
        for cart_item in cart_items:
            product = cart_item.product
            #product.quantity -= cart_item.quantity
            product.save()

        # Clear the cart
        cart_items.delete()

        # Redirect to payment success page
        #messages.success(request, 'Payment successful!')
        return redirect('payment_success')

    return render(request, 'payment.html')


def payment_success(request):
    return render(request, 'payment_success.html')