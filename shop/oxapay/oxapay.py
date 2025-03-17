import requests
import os

OXAPAY_API_KEY = "API_KEY"
OXAPAY_MERCHANT_ID = "MERCHANT_ID"
OXAPAY_API_URL = "c"

# Создание платежа
def create_payment(user_id, amount):
    if amount < 50:
        return None, "Минимальная сумма пополнения - 50 euro."

    data = {
        "merchant": OXAPAY_MERCHANT_ID,
        "amount": amount,
        "currency": "euro",
        "callback_url": f"https://elfhub.com/callback/",
        "custom": str(user_id)
    }

    headers = {
        "Authorization": f"Bearer {OXAPAY_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(f"{OXAPAY_API_URL}/invoice", json=data, headers=headers).json()

    if response.get("status") == "success":
        return response["data"]["pay_url"], response["data"]["id"]
    else:
        return None, response.get("message", "Ошибка при создании платежа.")

# Проверка статуса платежа

def check_payment_status(transaction_id):
    headers = {
        "Authorization": f"Bearer {OXAPAY_API_KEY}",
    }

    response = requests.get(f"{OXAPAY_API_URL}/invoice/{transaction_id}", headers=headers).json()

    if response.get("status") == "success":
        return response["data"]["status"]
    else:
        return None
