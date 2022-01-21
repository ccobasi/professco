from django.contrib import admin
from payments.models import Payment, PaymentIntent

admin.site.register(Payment)
admin.site.register(PaymentIntent)
