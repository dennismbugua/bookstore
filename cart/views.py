from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Book, Category
from .cart import Cart

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from store.models import Book, Category
from .cart import Cart

def cart_add(request, bookid):
	cart = Cart(request)  
	book = get_object_or_404(Book, id=bookid) 
	cart.add(book=book)
	
	# Check if it's an AJAX request
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		return JsonResponse({
			'status': 'success',
			'message': 'Book added to cart successfully!',
			'cart_total': len(cart),
			'book_title': book.name
		})
	
	return redirect('store:index')

def cart_update(request, bookid, quantity):
	cart = Cart(request) 
	book = get_object_or_404(Book, id=bookid) 
	cart.update(book=book, quantity=quantity)
	price = (book.price*quantity)
	
	# Check if it's an AJAX request
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		return JsonResponse({
			'status': 'success',
			'new_price': str(price),
			'cart_total': len(cart),
			'cart_total_price': str(cart.get_total_price())
		})

	return render(request, 'cart/price.html', {"price":price})

def cart_remove(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.remove(book)
    return redirect('cart:cart_details')

def total_cart(request):
	return render(request, 'cart/totalcart.html')

def cart_summary(request):

	return render(request, 'cart/summary.html')

def cart_details(request):
	cart = Cart(request)
	context = {
		"cart": cart,
	}
	return render(request, 'cart/cart.html', context)

