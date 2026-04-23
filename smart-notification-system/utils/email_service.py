# SMTP library to send mails
import smtplib
# to format the email content
from email.mime.text import MIMEText

def send_mail(subject:str, body:str):
    """
    Sends an email using Gmail SMTP server
    :param subject: email subject
    :param body: body of the mail
    :return: none
    """
    sender = "squarebrackets.sb@gmail.com"
    password = "nzuk uzft prko mqvp"

    receiver = "ravikant.tyagi.ms@gmail.com"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            # Start TLS encryption for secure connection
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("Email Sent Successfully...")
    except Exception as ex:
        print("Failed to send mail:",ex)
