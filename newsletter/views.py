# newsletter/views.py
from django.http import JsonResponse
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=400)

        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'error': 'This email is already subscribed.'}, status=400)

        # Save subscriber
        Subscriber.objects.create(email=email)
        return JsonResponse({'message': 'Subscription successful!'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
