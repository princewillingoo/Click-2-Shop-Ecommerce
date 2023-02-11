import requests
from decimal import Decimal
# import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order

# create the Stripe instance
api_key = settings.PAYSTACK_TEST_SECRETE_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    amount = order.get_total_cost()

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed'))

        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))
    
        # PayStack checkout session data
        session_data = {
            'email': order.email,
            'amount': int(amount),
            'callback_url': success_url
        }
        
        headers = {"authorization": f"Bearer {api_key}"}
        r = requests.post(url, headers=headers, data=session_data)
        response = r.json()
        if response["message"]:
            # redirect to PayStack payment form
            return redirect(response["data"]["authorization_url"], code=303)
        else:
            return render(request, 'payment/process.html', locals())

    else:
        return render(request, 'payment/process.html', locals())
    
    
def payment_completed(request):
    # order_id = request.session.get('order_id', None)
    # order = get_object_or_404(Order, id=order_id)
    
    # ref = request.GET.get('reference', '')
    # url = 'https://api.paystack.co/transaction/verify/{}'.format(ref)
    
    # headers = {"authorization": f"Bearer {api_key}"}
    # r = requests.get(url, headers=headers)
    # res = r.json()

    # if res['status']:
    #     # update order payment reference
    #     order.payment_ref = ref
    #     order.save()  
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html') 