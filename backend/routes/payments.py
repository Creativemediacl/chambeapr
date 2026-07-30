from fastapi import APIRouter, HTTPException
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

@router.get("/subscribe")
def get_subscription_link():
    return {
        "url": os.getenv("STRIPE_PAYMENT_LINK"),
        "price_id": os.getenv("STRIPE_PRICE_ID")
    }

@router.post("/create-checkout")
def create_checkout(email: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": os.getenv("STRIPE_PRICE_ID"), "quantity": 1}],
            mode="subscription",
            subscription_data={"trial_period_days": 30},
            customer_email=email,
            success_url="https://chambeapr.com/success",
            cancel_url="https://chambeapr.com/subscribe"
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
