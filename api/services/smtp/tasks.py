import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from task_manager.celery_app import app
from settings import settings


ssl_context = ssl.create_default_context()


sender= settings.SMTP_USER
host = settings.SMTP_HOST
port = settings.SMTP_PORT

user = settings.SMTP_USER
password = settings.SMTP_PASSWORD


@app.task
def send_email(receivers: list, subject: str,  html: str) -> None:
    """
        Sends an email with HTML content to the specified recipients.

        Args:
            receivers (list): A list of email addresses of the recipients.
            subject (str): The subject of the email.
            html (str): The HTML content of the email.

        Returns:
            None: This function does not return anything.

        Example:
            receivers = ['recipient1@example.com', 'recipient2@example.com']
            subject = 'Important Update'
            html = '<html><body><h1>Hello!</h1><p>This is an important update.</p></body></html>'
            send_email(receivers, subject, html)
    """
    with smtplib.SMTP_SSL(host, port, context=ssl_context) as server:
        server.login(user, password)

        msg = MIMEMultipart('alternative')

        for receiver in receivers:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = receiver

            part = MIMEText(html, 'html')
            msg.attach(part)

            server.sendmail(sender, receiver, msg.as_string())
