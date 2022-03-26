from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template import loader

def send_mails(review):
    subject = 'Confirm your email'
    sender = 'tanafus.mail@gmail.com'
    receiver = review.reviewer.email
    
    context = {
        'review': review,
    }
    body = loader.render_to_string('email_body.html', context=context)
    
    
    try:
        send_mail(
            subject,
            message='message',
            from_email=sender,
            recipient_list=[receiver],
            html_message=body,
        )
        return True

    except Exception as e:
        return False