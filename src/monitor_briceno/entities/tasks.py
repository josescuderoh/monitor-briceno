from monitor_briceno.celery import app
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# from datetime import date
import logging


@app.task()
def send_verification_email(user_id, domain):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        message = render_to_string('entities/acc_active_email.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activación de la cuenta'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except UserModel.DoesNotExist:
        logging.warning("El usuario para confirmación no existe en la base de datos: '%s'" % user_id)


# @app.task()
# def check_infrequent_users():
#     for user in get_user_model().objects.all():
#         last_activity = user.profile.last_activity.date()
#         today = date.today()
#         # Get difference
#         delta = today - last_activity
#         # Check delta time
#         if delta.days >= 15:
#             message = render_to_string('cooperacion/activity_notif.html',
#                                        {'user': user.first_name, })
#             mail_subject = 'Actualización de proyectos'
#             to_email = user.email
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             print("%s was notified" % user.email)
