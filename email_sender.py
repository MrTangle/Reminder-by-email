import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from keys import API_SENDGRID
from sanic.log import logger

SENDGRID_API_KEY = API_SENDGRID
EMAIL_FROM = 'fasturreminderapp@gmail.com'
EMAIL_TO = 'alexibanez86@gmail.com'


async def send_confirmation_email(title, description, date):
    with open('templates/confirmation_email.html', 'r', encoding='utf-8') as file:
        template = file.read()

    message = template.format(title=title, description=description, date=date)

    email = Mail(
        from_email=EMAIL_FROM,
        to_emails=EMAIL_TO,
        subject='Fastur Reminder App - Nuevo recordatorio',
        html_content=message
    )

    try:
        sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY', SENDGRID_API_KEY))
        response = sg.send(email)
        logger.info('Correo electrónico enviado exitosamente.')
    except Exception as e:
        logger.error('Error al enviar el correo electrónico: {}'.format(str(e)))