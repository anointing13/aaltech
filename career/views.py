from django.shortcuts import render, redirect
from .forms import CareerForm


def career_view(request):
    if request.method == 'POST':
        form = CareerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('career_success')  # Redirect to a success page after submission
    else:
        form = CareerForm()

    return render(request, 'career/career_form.html', {'form': form})


def career_success(request):
    return render(request, 'career/success.html')

