# from django.conf import settings
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from orders.models import Order


# @csrf_exempt
# def stripe_webhook(request):
#     print(request.body)
#     print("###########################################")
#     print(request.headers['x-paystack-signature'])
#     print("###########################################")
    
#     return HttpResponse(status=200)