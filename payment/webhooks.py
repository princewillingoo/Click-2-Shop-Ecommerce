import hmac
import hashlib
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order

secret = settings.PAYSTACK_TEST_SECRETE_KEY


@csrf_exempt
def paystack_webhook(request):
    payload = request.body
    sig_header = request.headers['x-paystack-signature']
    body = None
    event = None

    try:
        hash = hmac.new(secret.encode('utf-8'), payload, digestmod=hashlib.sha512).hexdigest()
        if hash == sig_header:
            body_unicode = payload.decode('utf-8')
            body = json.loads(body_unicode)
            event = body['event']
        else:
            raise Exception
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except KeyError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except:
        # Invalid signature
        return HttpResponse(status=400)

    if event == 'charge.success':
        data, order_id = body["data"], body['data']['metadata']['order_id']

        if (data["status"] == 'success') and (data["gateway_response"] == "Successful"):
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid
            order.paid = True
            order.save(force_update=True)
            print("PAID")

    return HttpResponse(status=200)
