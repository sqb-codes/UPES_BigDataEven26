import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.email_service import send_mail

def send_notification(event, priority, reason):
    """
    Decides how to send notification based on priority
    :param event: type of event - login, transaction, order
    :param priority: LOW, IGNORE, MEDIUM
    :param reason: reason of sending mail
    :return: none
    """

    subject = f"{priority} : Priority Alert"
    body = f"""
    Smart Notification Alert
    Event Details:
    {event}
    
    Priority: {priority}
    Reason: {reason}
    """
    send_mail(subject, body)
    print("Notification Triggered...")
