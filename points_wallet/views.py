from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Wallet, Withdrawal, Transaction
from .utils import handle_daily_login, handle_purchase, handle_withdrawal
from product.models import Product

@login_required
def wallet_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all()

    handle_daily_login(request.user)

    return render(request, 'points_wallet/wallet.html', {'wallet': wallet, 'transactions': transactions})

@login_required
def withdraw_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        mobile_money_number = request.POST.get("mobile_money_number")
        points = int(request.POST.get("points"))

        wallet, created = Wallet.objects.get_or_create(user=request.user)

        try:
            handle_withdrawal(wallet, full_name, mobile_money_number, points)
            messages.success(request, "Withdrawal successful.")
            return redirect("points_wallet:wallet_view")
        except ValueError as e:
            return render(request, "points_wallet/wallet.html", {
                "error_message": str(e),
                "full_name": full_name,
                "mobile_money_number": mobile_money_number,
                "points": points,
            })

    withdrawals = Withdrawal.objects.filter(wallet__user=request.user).order_by('-created_at')

    return render(request, "points_wallet/wallet.html", {"withdrawals": withdrawals})

@login_required
def withdrawal_history(request):
    withdrawals = Withdrawal.objects.filter(wallet__user=request.user)

    return render(request, 'points_wallet/withdrawal_history.html', {'withdrawals': withdrawals})

@login_required
def purchase_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    amount = product.price

    handle_purchase(request.user, amount)

    return redirect('points_wallet:wallet_view')
