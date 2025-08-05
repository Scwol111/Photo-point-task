""" Module for sending messages to users
"""
import smtplib
from email.message import EmailMessage

import environ
import requests
from mailersend import sms_sending


def get_env(env_name: str) -> str:
    """Get enviroment string

    Args:
        env_name (str): name of enviroment

    Returns:
        str: value of 
    """
    env = environ.Env(
        # set casting, default value
        DEBUG=(bool, False),
        ALLOWED_HOSTS=(list, []),
    )
    environ.Env.read_env('.env')
    result = env(env_name, str)
    if result is None:
        raise ValueError(f"Enviroment {env_name} not found")
    return result

def send_email(user_email: str, message: str):
    """Send email to user

    Args:
        user_email (str): email of user
        message (str): message string
    """
    email = EmailMessage()
    email_from = get_env('FROM_EMAIL')
    email['from'] = email_from
    email['to'] = user_email
    email['subject'] = get_env('MAIL_SUBJECT')
    email.set_content(message)

    with smtplib.SMTP(host=get_env('EMAIL_HOST'), port=int(get_env('EMAIL_PORT'))) as smtp:
        smtp.starttls()
        smtp.login(email_from, get_env("EMAIL_PASSWORD"))
        errors = smtp.send_message(email)
        if len(errors) > 0:
            raise Exception(f'Send email failed. Errors: {errors}')

def send_sms(user_phone: str, message: str):
    """Send SMS to user

    Args:
        user_phone (str): user phone
        message (str): message to send
    """
    mailer = sms_sending.NewSmsSending(get_env('MAILERSEND_API_KEY'))
    mailer.send_sms(get_env("MAILSEND_NUMBER"), [user_phone], message)

def send_tg_message(user_tg_chat_id: str, message: str):
    """Send message via telegramm 

    Args:
        user_tg_chat_id (str): user chat to send
        message (str): message
    """
    send_message_url = f'https://api.telegram.org/bot{get_env("TELEGRAMM_BOT_TOKEN")}/sendMessage'
    payload = {
        'chat_id': user_tg_chat_id,
        'text': message
    }
    response = requests.post(send_message_url, data=payload, timeout=300)
    if not (200 <= response.status_code < 300):
        raise Exception(f'Sending tg message error: {response.json()}')
