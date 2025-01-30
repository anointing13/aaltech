from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .utils import handle_daily_login, handle_purchase, handle_withdrawal
from product.models import Product  # Correct
from django.contrib import messages
from .models import Withdrawal

@login_required
def wallet_view(request):
    # Get user's wallet and related transactions
    wallet = request.user.wallet
    transactions = wallet.transactions.all()

    # Optionally: Call the daily login bonus function (e.g., each time the user visits their wallet)
    handle_daily_login(request.user)

    # Render the wallet view
    return render(request, 'points_wallet/wallet.html', {'wallet': wallet, 'transactions': transactions})



@login_required
def withdraw_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        mobile_money_number = request.POST.get("mobile_money_number")
        points = int(request.POST.get("points"))

        wallet = request.user.wallet

        try:
            handle_withdrawal(wallet, full_name, mobile_money_number, points)
            messages.success(request, "Withdrawal successful.")
            return redirect("points_wallet:wallet_view")  # Redirect to wallet view
        except ValueError as e:
            # Pass error message to template along with form data
            return render(request, "points_wallet/wallet.html", {
                "error_message": str(e),
                "full_name": full_name,
                "mobile_money_number": mobile_money_number,
                "points": points,
            })

    # Fetch all withdrawals for the logged-in user (or associated wallet)
    withdrawals = Withdrawal.objects.filter(wallet__user=request.user).order_by('-created_at')

    # Render wallet template with withdrawals data
    return render(request, "points_wallet/wallet.html", {
        "withdrawals": withdrawals
    })


@login_required
def withdrawal_history(request):
    # Fetch the withdrawal records for the logged-in user
    withdrawals = Withdrawal.objects.filter(wallet__user=request.user)

    return render(request, 'points_wallet/withdrawal_history.html', {'withdrawals': withdrawals})


@login_required
def purchase_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product or return 404 if not found
    amount = product.price

    # Call the handle_purchase function to add points for the user purchase
    handle_purchase(request.user, amount)

    # Optionally redirect to some confirmation page or back to the wallet
    return redirect('wallet_view')  # Redirect back to the wallet view or wherever you need


