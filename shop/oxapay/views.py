from oxapay import check_payment_status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models import Payment


@csrf_exempt
def oxapay_callback(request):
    if request.method == "POST":
        data = request.POST
        transaction_id = data.get("id")
        status = data.get("status")

        payment = Payment.objects.filter(transaction_id=transaction_id, status="pending").first()

        if payment:
            if status == "completed":
                payment.status = "completed"
                payment.user.balance += payment.amount
                payment.user.save()
                payment.save()
            elif status == "failed":
                payment.status = "failed"
                payment.save()

        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid request"}, status=400)