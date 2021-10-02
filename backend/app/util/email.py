import logging
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from jose import jwt
import emails
from emails.template import JinjaTemplate
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.core import config, security


conf = ConnectionConfig(
    MAIL_USERNAME=config.SMTP_USER,
    MAIL_PASSWORD=config.SMTP_PASSWORD,
    MAIL_FROM=config.EMAILS_FROM_EMAIL,
    MAIL_PORT=1025,
    MAIL_SERVER="localhost",
    MAIL_FROM_NAME=config.EMAILS_FROM_NAME,
    MAIL_TLS=False,
    MAIL_SSL=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "email_templates" / "build",
)


async def send_plaintext_email(
    email_to: str,
    subject: str = "",
    raw_text: str = "",
    environment: Dict[str, Any] = {},
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=raw_text,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    logging.info(f"sent email {message} to {email_to}")


async def send_template_email(
    email_to: str,
    subject: str = "",
    template_file: str = "",
    environment: Dict[str, Any] = {},
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=environment,
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_file)
    logging.info(f"sent email {message} to {email_to}")


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=config.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        security.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, security.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
