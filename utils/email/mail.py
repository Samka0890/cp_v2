import smtplib
from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from settings.configuration import EMAIL
from settings.configuration import ADMINS


def send_mail_error(error, id, location):

    msg = MIMEMultipart()
    now = datetime.now()

    msg['Subject'] = 'Киоск дээр алдаа гарлаа.'
    msg['From'] = 'developer.of.nirge@gmail.com'
    msg['To'] = (', ').join(ADMINS)

    body = (
        '\nКиоск ID : ' +
        id + '\nlocation : ' +
        location + '\nХугацаа : ' +
        str(now.strftime("%Y-%m-%d %H:%M:%S")) +
        ' ' + "\nERROR_TYPE : "
        + str(error)
    )

    body = MIMEText(body)
    msg.attach(body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # TODO мэйлийн мэдээлэл энд байх ёсгүй
        server.login(EMAIL['mail'], EMAIL['password'])
        server.send_message(msg)
        server.quit()
        print('Email successfully')

    except Exception as err:
        print('An error occurred while sending the email ', err)
