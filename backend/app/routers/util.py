from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlmodel import Session

import stripe
from pydantic import BaseModel
from stripe.api_resources import payment_method

from app import deps
from app.database import get_session
from app.models import User
from app.util.email import send_template_email, send_plaintext_email


router = APIRouter(prefix="/util", tags=["util"])


@router.post("/create-setup-intent")
def create_setup_intent(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    intent = stripe.SetupIntent.create(
        customer=current_user.stripe_customer_id, payment_method_types=["card"]
    )
    return {"client_secret": intent.client_secret}


@router.get("/send-email")
async def test_send_email():
    # await send_plaintext_email(
    #     email_to="tomhill98@me.com",
    #     subject="Hello World",
    #     raw_text="<h1>Welcome :)</h1>",
    # )
    await send_template_email(
        email_to="tomhill98@me.com",
        subject="Welcome!",
        template_file="welcome.html",
        environment={
            "project_name": "demo",
            "username": "tomhill",
            "password": "hunter4",
        },
    )
    return {"message": "email has been sent"}
