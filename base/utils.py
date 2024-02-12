from django.core.mail import send_mail
from django.conf import settings

def send_email_token(email,token):
    try:
        subject = "Verify your email"
        message = f"Hi click on the link to verify your email http://127.0.0.1:8000/verify/{token}/{email}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(e)
        return False