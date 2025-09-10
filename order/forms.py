from django import forms
from .models import Order
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class OrderCreateForm(forms.ModelForm):
	PAYMENT_METHOD_CHOICES = (
		('Card Payment', 'Card Payment'),
		('PayPal', 'PayPal')
	)

	payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect())
	country = CountryField(default='KE').formfield(widget=CountrySelectWidget(attrs={
		'class': 'form-control',
		'id': 'id_country',
		'autocomplete': 'off',
		'style': 'font-weight: 500;'
	}))

	class Meta:
		model = Order
		fields = ['name', 'email', 'phone', 'address', 'country', 'zip_code', 'payment_method', 'account_no', 'transaction_id']
		widgets = {
			'name': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter your full name',
				'autocomplete': 'off'
			}),
			'email': forms.EmailInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter your email address',
				'autocomplete': 'new-email'
			}),
			'phone': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter your phone number',
				'autocomplete': 'new-tel'
			}),
			'address': forms.Textarea(attrs={
				'class': 'form-control',
				'placeholder': 'Enter your full address',
				'rows': 3,
				'autocomplete': 'new-address'
			}),
			'zip_code': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter postal/zip code',
				'autocomplete': 'off'
			}),
			'account_no': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter card number or PayPal email',
				'autocomplete': 'off'
			}),
			'transaction_id': forms.NumberInput(attrs={
				'class': 'form-control',
				'placeholder': 'Enter CVV or PayPal transaction ID',
				'autocomplete': 'off'
			})
		}
