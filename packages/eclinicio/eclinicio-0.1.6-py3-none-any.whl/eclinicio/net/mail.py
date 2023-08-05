import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os


def create_attachment(path):
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)

    if path.endswith('.zip'):
        with open(path, 'rb') as zf:
            attachment = MIMEBase('application', 'zip')
            attachment.set_payload(zf.read())
            encoders.encode_base64(attachment)
    else:
        with open(path) as fp:
            attachment = MIMEText(fp.read(), _subtype=subtype)
    return attachment


def compose_mail(subject, body, sender, recipient, preamble=None, attachment_path=None):
    """Create mail message"""

    message = MIMEMultipart()
    message['Subject'] = subject
    message['To'] = recipient
    message['From'] = sender
    message.attach(MIMEText(body))

    if preamble is not None:
        message.preamble = preamble

    if attachment_path is not None and os.path.exists(attachment_path):
        attachment = create_attachment(attachment_path)
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=os.path.basename(attachment_path))
        message.attach(attachment)
    return message


def send_mail(message, password):
    sender = message['From']
    recipient = message['To']
    smtp = smtplib.SMTP('smtp.googlemail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender, password)
    smtp.sendmail(sender, recipient, message.as_string())
    smtp.quit()
    return True


if __name__ == '__main__':
    message = compose_mail(
        subject='Greetings',
        body='Hello guys',
        sender='nabizy@gmail.com',
        recipient='someone@example.com',
        preamble='no-reply',
        attachment_path='some_file.zip')
