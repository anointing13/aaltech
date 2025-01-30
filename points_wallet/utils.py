from datetime import date

from .models import Transaction, Withdrawal


def handle_daily_login(user):
    wallet = user.wallet
    today = date.today()

    if wallet.last_login_date != today:
        wallet.points += 7
        wallet.last_login_date = today
        wallet.save()

        Transaction.objects.create(wallet=wallet, transaction_type='LOGIN_BONUS', points=7)


def handle_purchase(user, amount):
    wallet = user.wallet

    # Add 20 points for any purchase
    wallet.points += 20
    Transaction.objects.create(wallet=wallet, transaction_type='PURCHASE_BONUS', points=20)

    # Add 1000 points for purchases >= GHS 10,000
    if amount >= 10000:
        wallet.points += 1000
        Transaction.objects.create(wallet=wallet, transaction_type='BIG_PURCHASE_BONUS', points=1000)

    wallet.save()


def handle_withdrawal(wallet, full_name, mobile_money_number, points):
    if wallet.points < points:
        raise ValueError("Insufficient points for withdrawal.")

    wallet.points -= points
    wallet.save()

    Withdrawal.objects.create(
        wallet=wallet,
        full_name=full_name,
        mobile_money_number=mobile_money_number,
        points=points,
    )
