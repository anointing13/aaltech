from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import FormView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send welcome email after user registration
            subject = 'Welcome to ABOVE ALL TECHNOLOGY LIMITED! 🚀'
            message = f"""
            Hi {user.first_name},

            Welcome to ABOVE ALL TECHNOLOGY! We're thrilled to have you join our community. 

            Thank you for registering and taking the first step towards an amazing experience with us. 
            
            If you ever need assistance, feel free to reach out — we're here to help!

            Get ready to explore new opportunities with ABOVE ALL TECHNOLOGY.

            Best regards,
            The ABOVE ALL TECHNOLOGY LIMITED Team
            """
            recipient_list = [user.email]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

            # Set the backend attribute before logging in
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)  # Log the user in after successful signup

            return redirect('home')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Check if "Remember me" is checked in the form
            remember_me = request.POST.get('remember_me', None)

            if remember_me:
                # Keep the user logged in for 2 weeks (1209600 seconds)
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                # Session expires when the browser is closed
                request.session.set_expiry(0)

            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


# accounts/views.py
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        # Call the parent form_valid to ensure the default process runs
        response = super().form_valid(form)
        # Send the custom email
        self.send_custom_email(form)
        return response

    def send_custom_email(self, form):
        user_email = form.cleaned_data.get('email')
        # Get the user(s) associated with the email
        users = form.get_users(user_email)
        if users:
            user = next(iter(users), None)  # Get the first user
            if user:
                subject = 'Password Reset Requested'
                context = {
                    'email': user_email,
                    'user': user,
                    'protocol': self.request.scheme,
                    'domain': self.request.get_host(),
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Use this for uid
                    'token': default_token_generator.make_token(user),  # Use this to create a token
                    'site_name': 'aatech.com',
                }
                # Render the email body from the template
                email_body = render_to_string(self.email_template_name, context)
                # Send the email
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email],
                    fail_silently=False,
                )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, request, *args, **kwargs):
        # Decode the uid from the URL
        self.uid = force_str(urlsafe_base64_decode(kwargs['uidb64']))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the uid to the template if needed
        context['uid'] = self.uid
        return context
