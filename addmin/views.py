# addmin/views.py

from django.shortcuts import render
from django.http import JsonResponse
from cruds.models import Becholer, Wedding, Reception
from event.models import Contact
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # This is for demonstration. Use more secure methods in production.
def chart_order(request, order_id):
    if request.method == 'POST':
        try:
            # Find the order based on order_id
            order = Becholer.objects.filter(oid=order_id).first() or \
                    Wedding.objects.filter(oid=order_id).first() or \
                    Reception.objects.filter(oid=order_id).first()

            if order:
                # Decrease the relevant order count
                counts = {
                    'bachelorParty': Becholer.objects.filter(status='Pending').count(),
                    'wedding': Wedding.objects.filter(status='Pending').count(),
                    'reception': Reception.objects.filter(status='Pending').count(),
                }
                return JsonResponse(counts)

            return JsonResponse({'error': 'Order not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def order_stats(request):
    # Get counts of each model
    bachelor_count = Becholer.objects.count()
    wedding_count = Wedding.objects.count()
    reception_count = Reception.objects.count()

    # Create a response dictionary
    data = {
        'bachelorParty': bachelor_count,
        'wedding': wedding_count,
        'reception': reception_count,
    }

    return JsonResponse(data)


def index(request):
    return render(request, 'addmin/addmin-index.html')

def uploadoption(request):
    return render(request, 'addmin/uploadoption.html')

