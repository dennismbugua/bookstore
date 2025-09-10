from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import paypalrestsdk
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .pdfcreator import renderPdf
import uuid
import logging

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order):
    """Send a beautiful confirmation email to the customer"""
    try:
        subject = f'Order Confirmation - Your Bookstore Purchase #{order.id}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order.email]
        
        # Create email context
        context = {
            'order': order,
            'order_items': order.items.all(),
            'subtotal': order.payable - settings.SHIPPING_COST,
            'shipping_cost': settings.SHIPPING_COST,
            'total': order.payable,
            'customer_name': order.name,
        }
        
        # Render HTML email template
        html_content = render_to_string('order/emails/order_confirmation.html', context)
        text_content = strip_tags(html_content)
        
        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=to_email
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send()
        logger.info(f"Order confirmation email sent successfully to {order.email} for order #{order.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order confirmation email for order #{order.id}: {str(e)}")
        return False

def order_create(request):
	cart = Cart(request)
	if request.user.is_authenticated:
		customer = get_object_or_404(User, id=request.user.id)
		form = OrderCreateForm(request.POST or None, initial={"name": customer.first_name, "email": customer.email})
		if request.method == 'POST':
			if form.is_valid():
				# Calculate total with shipping
				cart_total = cart.get_total_price()
				total_with_shipping = cart_total + settings.SHIPPING_COST
				
				order = form.save(commit=False)
				order.customer = User.objects.get(id=request.user.id)
				order.payable = total_with_shipping
				order.totalbook = len(cart) # len(cart.cart) // number of individual book
				order.save()

				for item in cart:
					OrderItem.objects.create(
						order=order, 
						book=item['book'], 
						price=item['price'], 
						quantity=item['quantity']
						)
				cart.clear()
				return render(request, 'order/successfull.html', {'order': order})

			else:
				messages.error(request, "Fill out your information correctly.")

		if len(cart) > 0:
			return render(request, 'order/order.html', {"form": form})
		else:
			return redirect('store:books')
	else:
		return redirect('store:signin')
			
def order_list(request):
	my_order = Order.objects.filter(customer_id = request.user.id).order_by('-created')
	paginator = Paginator(my_order, 5)
	page = request.GET.get('page')
	myorder = paginator.get_page(page)

	return render(request, 'order/list.html', {"myorder": myorder})

def order_details(request, id):
	order_summary = get_object_or_404(Order, id=id)

	if order_summary.customer_id != request.user.id:
		return redirect('store:index')

	orderedItem = OrderItem.objects.filter(order_id=id)
	context = {
		"o_summary": order_summary,
		"o_item": orderedItem
	}
	return render(request, 'order/details.html', context)

class pdf(View):
    def get(self, request, id):
        try:
            query=get_object_or_404(Order,id=id)
        except:
            Http404('Content not found')
        context={
            "order":query
        }
        article_pdf = renderPdf('order/pdf.html',context)
        return HttpResponse(article_pdf,content_type='application/pdf')

def paypal_payment_process(request, order_id):
    """Process PayPal payment for an order"""
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    
    # Generate unique invoice number
    invoice_id = f"INV-{order.id}-{uuid.uuid4().hex[:8]}"
    
    # Calculate shipping cost (using the same constant as in template)
    SHIPPING_COST = settings.SHIPPING_COST
    SHIPPING_COST = 100
    subtotal = order.payable - SHIPPING_COST  # order.payable already includes shipping from cart
    
    # PayPal form data with all required fields
    paypal_dict = {
        'cmd': '_xclick',  # Required PayPal command
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{subtotal:.2f}',  # Subtotal without shipping
        'shipping': f'{SHIPPING_COST:.2f}',  # Shipping cost
        'item_name': f'Bookstore Order #{order.id}',
        'item_number': str(order.id),
        'invoice': invoice_id,
        'currency_code': settings.PAYPAL_CURRENCY_CODE,
        'no_note': '1',  # No note from buyer
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return': request.build_absolute_uri(reverse('order:paypal_success', kwargs={'order_id': order.id})),
        'cancel_return': request.build_absolute_uri(reverse('order:paypal_cancel', kwargs={'order_id': order.id})),
        'custom': str(order.id),  # Pass the order ID as string
        'rm': '2',  # Return method: POST
        'charset': 'utf-8',  # Character encoding
        'lc': 'US',  # Locale code
        'bn': 'PP-BuyNowBF:btn_buynowCC_LG.gif:NonHostedGuest',  # Build notation
    }
    
    # Debug: Print the PayPal data (remove in production)
    print("=" * 50)
    print("PAYPAL FORM DATA BEING SENT:")
    print("=" * 50)
    for key, value in paypal_dict.items():
        print(f"  {key}: {value}")
    print("=" * 50)
    print(f"PayPal Action URL: https://www.sandbox.paypal.com/cgi-bin/webscr")
    print("=" * 50)
    
    # Create PayPal form manually for Django 5 compatibility
    try:
        form = PayPalPaymentsForm(initial=paypal_dict)
        form_fields = form.initial
    except Exception as e:
        print(f"PayPal form error: {e}")
        # Fallback: create form fields manually
        form_fields = paypal_dict
    
    # Get PayPal action URL for sandbox
    paypal_action_url = "https://www.sandbox.paypal.com/cgi-bin/webscr"
    
    context = {
        'order': order,
        'form_fields': form_fields,
        'paypal_action_url': paypal_action_url,
    }
    return render(request, 'order/paypal_payment.html', context)

def paypal_debug(request, order_id):
    """Debug view to show PayPal form data"""
    order = get_object_or_404(Order, id=order_id)
    
    # Generate the same data as paypal_payment_process
    invoice_id = f"INV-{order.id}-{uuid.uuid4().hex[:8]}"
    
    # Calculate shipping cost breakdown
    SHIPPING_COST = 100
    subtotal = order.payable - SHIPPING_COST
    
    # Build return URLs for local development
    base_url = f"{'https' if request.is_secure() else 'http'}://{request.get_host()}"
    success_url = f"{base_url}{reverse('order:paypal_success', kwargs={'order_id': order.id})}"
    cancel_url = f"{base_url}{reverse('order:paypal_cancel', kwargs={'order_id': order.id})}"
    ipn_url = f"{base_url}{reverse('paypal-ipn')}"
    
    paypal_dict = {
        'cmd': '_xclick',
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{subtotal:.2f}',  # Subtotal without shipping
        'shipping': f'{SHIPPING_COST:.2f}',  # Shipping cost
        'item_name': f'Bookstore Order #{order.id}',
        'invoice': invoice_id,
        'currency_code': settings.PAYPAL_CURRENCY_CODE,
        'notify_url': ipn_url,
        'return': success_url,
        'cancel_return': cancel_url,
        'custom': str(order.id),
    }
    
    paypal_action_url = "https://www.sandbox.paypal.com/cgi-bin/webscr"
    
    context = {
        'order': order,
        'form_fields': paypal_dict,
        'paypal_action_url': paypal_action_url,
    }
    return render(request, 'order/paypal_debug.html', context)

@csrf_exempt
def paypal_success(request, order_id):
    """Handle successful PayPal payment"""
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    
    # Send confirmation email to customer
    email_sent = send_order_confirmation_email(order)
    if email_sent:
        logger.info(f"Order confirmation email sent for order #{order.id}")
        messages.success(request, 'Your payment was successful! Order has been confirmed. A confirmation email has been sent.')
    else:
        logger.warning(f"Failed to send confirmation email for order #{order.id}")
        messages.success(request, 'Your payment was successful! Order has been confirmed.')
    
    return render(request, 'order/paypal_success.html', {'order': order, 'email_sent': email_sent})

@csrf_exempt
def paypal_cancel(request, order_id):
    """Handle cancelled PayPal payment"""
    order = get_object_or_404(Order, id=order_id)
    messages.warning(request, 'Payment was cancelled. You can try again.')
    return render(request, 'order/paypal_cancel.html', {'order': order})

@csrf_exempt
def create_paypal_payment(request):
    """AJAX endpoint to create PayPal payment"""
    if request.method == 'POST':
        try:
            cart = Cart(request)
            customer = get_object_or_404(User, id=request.user.id)
            
            # Calculate total with shipping
            SHIPPING_COST = 100
            cart_total = cart.get_total_price()
            total_with_shipping = cart_total + SHIPPING_COST
            
            # Create order first
            order = Order.objects.create(
                customer=customer,
                name=request.POST.get('name', customer.first_name),
                email=request.POST.get('email', customer.email),
                phone=request.POST.get('phone', ''),
                address=request.POST.get('address', ''),
                country=request.POST.get('country', 'KE'),
                zip_code=request.POST.get('zip_code', ''),
                payment_method='PayPal',
                account_no='',  # PayPal doesn't need account number
                transaction_id=0,  # Will be updated after payment
                payable=total_with_shipping,
                totalbook=len(cart)
            )
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item['book'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Generate PayPal payment URL
            payment_url = reverse('order:paypal_payment', kwargs={'order_id': order.id})
            
            return JsonResponse({
                'success': True,
                'payment_url': payment_url,
                'order_id': order.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def check_payment_status(request, order_id):
    """Check if PayPal payment has been completed"""
    try:
        order = get_object_or_404(Order, id=order_id)
        return JsonResponse({
            'paid': order.paid,
            'order_id': order.id,
            'transaction_id': order.transaction_id if order.paid else None
        })
    except Order.DoesNotExist:
        return JsonResponse({'paid': False, 'error': 'Order not found'})

# PayPal IPN signal handler
def paypal_payment_received(sender, **kwargs):
    """Handle IPN signals from PayPal"""
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            order_id = ipn_obj.custom
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.transaction_id = ipn_obj.txn_id
            order.save()
        except Order.DoesNotExist:
            pass

# Connect the signal
valid_ipn_received.connect(paypal_payment_received)
