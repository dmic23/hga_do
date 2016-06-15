# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings
# from django.contrib.auth.forms import PasswordResetForm
# from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from io import BytesIO
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from users.models import User, StudentPracticeLog
from django.utils import timezone



@shared_task
def send_create_email(user):
    subject, from_email, to, bcc = 'Welcome to Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s! Welcome to Hirsch Guitar Academy  You\'re account must be activated by Hirsch Guitar Academy' %user.first_name
    html_content = '<p>Hi %s!</hp><br/><p> Welcome to Hirsch Guitar Academy!</p><br/><p>You\'re account will be activated shortly on approval from Hirsch Guitar Acacdemy. You will receive a confirmation email once complete.</p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_active_email(user):
    subject, from_email, to, bcc = 'Hirsch Guitar Academy Activation', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s! Welcome to Hirsch Guitar Academy  Login here: www.hirschguitaracademy.com' %user.first_name
    html_content = '<p>Hi %s!</hp><br/><p> Welcome to Hirsch Guitar Academy!</p><br/><p>You\'re account has been activated. Login here: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_update_email(user):
    subject, from_email, to, bcc = 'Updates from Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
    text_content = 'Hi %s!  You have new updates at Hirsch Guitar Academy. Login here: hirschguitaracademy.com Thank you, Hirsch Guitar Academy' %user.first_name
    html_content = '<p>Hi %s!</hp><br/><p>You have new updates at Hirsch Guitar Academy! Login here to see them: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@periodic_task
def send_practice_reminder():
    prac_since = timezone.now() - timezone.timedelta(days=3, hours=5)
    print "Prac Since === %s" %prac_since
    user_practice = User.objects.exclude(student_log__practice_date__gt=prac_since).distinct() 
    for user in user_practice:
        subject, from_email, to, bcc = 'Practice Update from Hirsch Guitar Academy', 'hgatestacct@gmail.com', user.email, 'hgatestacct@gmail.com'
        text_content = 'Hi %s!  Practice makes perfect. It\'s been more than 3 days since your last practice. Login to add your practice. Login here: hirschguitaracademy.com Thank you, Hirsch Guitar Academy' %user.first_name
        html_content = '<p>Hi %s!</hp><br/><p>Practice makes perfect. It\'s been more than 3 days since your last practice. Login to add your practice! Login here: <a href="hirschguitaracademy.com">hirschguitaracademy.com</a></p><br/><p>Thank you,</p><br/><p>Hirsch Guitar Academy</p>' %user.first_name
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], [bcc])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

