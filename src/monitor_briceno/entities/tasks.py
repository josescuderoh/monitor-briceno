# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from datetime import date
import logging
from monitor_briceno.celery import app
from projects.models import Project


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
#     try:
#         for user in get_user_model().objects.all():
#             last_activity = user.last_activity.date()
#             today = date.today()
#             # Get difference
#             delta = today - last_activity
#             # Check delta time
#             if delta.days >= 15 and not all(project.closed for project in Project.objects.filter(created_by=user)):
#                 message = render_to_string('entities/activity_notif.html',
#                                            {'user': user.get_short_name(), })
#                 mail_subject = 'Actualización de proyectos'
#                 to_email = user.email
#                 email = EmailMessage(mail_subject, message, to=[to_email])
#                 email.send()
#                 return("%s was notified" % user.email)
#     except:
#         return("Error was found")
