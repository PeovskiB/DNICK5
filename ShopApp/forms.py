from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiry_date = forms.CharField(label='Expiry Date', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=3)
