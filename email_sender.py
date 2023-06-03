import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from keys import API_SENDGRID

SENDGRID_API_KEY = API_SENDGRID
EMAIL_FROM = 'fasturreminderapp@gmail.com'
EMAIL_TO = ['alexibanez86@gmail.com', 'garciavictor1111@gmail.com']


async def send_confirmation_email(title, description, date):
    message = f"Se ha creado un nuevo recordatorio:\n\n" \
              f"Título: {title}\n" \
              f"Descripción: {description}\n" \
              f"Fecha: {date}\n"

    email = Mail(
        from_email=EMAIL_FROM,
        to_emails=EMAIL_TO,
        subject='Fastur Reminder App - Nuevo recordatorio',
        plain_text_content=message
    )

    try:
        sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY', SENDGRID_API_KEY))
        response = sg.send(email)
        print('Correo electrónico enviado exitosamente.')
    except Exception as e:
        print('Error al enviar el correo electrónico:', str(e))