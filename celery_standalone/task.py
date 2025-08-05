""" Celery tasks to sending messages to user
"""
from enum import IntEnum

from celery import Celery

from send_messages import send_email, send_sms, send_tg_message, get_env

class SendMessageResult(IntEnum):
    """Message sending result
    """
    SEND_EMAIL = 0
    SEND_SMS = 1
    SEND_TG = 2
    NOT_SEND = 3


app = Celery('send-user-messages',
             broker=get_env('CELERY_BROKER_URL'),
             result_backend=get_env('CELERY_RESULT_BACKEND'),
             broker_connection_retry_on_startup=False)

@app.task(name='send_message')
def send_user_message(user_email: str, user_phone: str, user_tg: str, message: str) -> SendMessageResult:
    """Task to send message to user

    Args:
        user_email (str): user email
        user_phone (str): user phone number
        user_tg (str): user tg account
        message (str): message string

    Returns:
        SendMessageResult: result of task
    """
    try:
        send_email(user_email, message)
        return SendMessageResult.SEND_EMAIL
    except: pass
    try:
        send_sms(user_phone, message)
        return SendMessageResult.SEND_SMS
    except: pass
    try:
        send_tg_message(user_tg, message)
        return SendMessageResult.SEND_TG
    except: pass
    return SendMessageResult.NOT_SEND
