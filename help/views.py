from django.shortcuts import render


def help_page(request):
    # Example dynamic data for HELP
    faqs = [
        {"question": "How do I reset my password?", "answer": "Click on 'Forgot Password' on the login page."},
        {"question": "How do I contact support?", "answer": "You can contact support at support@aatech.com."},
        {"question": "Where can I find other services of Above All Technology Limited?", "answer": "Click on your name to dropdown the list and select the service of your choice."},
        {"question": "Where can I find my orders?", "answer": "Click on SnapShop to locate My Orders."},
    ]
    return render(request, 'help.html', {'faqs': faqs})
