from celery import shared_task
from accounts.models import User
from django.conf import settings
from django.core.mail import EmailMessage



@shared_task
def mail_send(mail_content, x=None):
    to_emails = []
    users_list = User.objects.all()
    for usr in users_list:
        if usr.username != 'admin':
            to_emails.append(usr.email)

    subject = 'New announcement on LMS'
    message = mail_content
    email_from = settings.EMAIL_HOST_USER
    recipient_list = to_emails
    for i in recipient_list:
        email = EmailMessage(subject, message, email_from, [i])
        email.content_subtype = "html"
        if x:
            email.attach_file(x)
        email.send()

    return "successfully done!"
