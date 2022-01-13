from django.shortcuts import render
from django.core.exceptions import ValidationError
from payments.models import Payment, PaymentIntent
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from courses.models import Course
import json
from decimal import Decimal
import os

stripe_api_key = os.environ.get("STRIPE_APIKEY")
endpoint_secret = ""


class PaymentHandler(APIView):

    def post(self, request):

        if request.body:
            body = json.loads(request.body)
            if body and len(body):
                # fetch course detail as line_items
                courses_line_items = []
                cart_course = []
                for item in body:
                    try:
                        course = Course.objects.get(course_uuid=item)

                        line_item = {
                            'price_data': {
                                'currency': '#',
                                'unit_amount': int(course.price*100),
                                'product_data': {
                                    'name': course.title,

                                },
                            },
                            'quantity': 1,
                        }

                        courses_line_items.append(line_item)
                        cart_course.append(course)

                    except Course.DoesNotExist:
                        pass
                    except ValidationError:
                        pass

            else:
                return Response(status=400)
        else:
            return Response(status=400)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=courses_line_items,
            mode='payment',
            success_url='http://localhost:3000/',
            cancel_url="http://localhost:3000/",

        )

        intent = PaymentIntent.objects.create(
            payment_intent_id=checkout_session.payment_intent,
            checkout_id=checkout_session.id,
            user=request.user,
        )

        for course in cart_course:
            intent.courses.add(course)

        return Response({"url": checkout_session.url})
