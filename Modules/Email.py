from email.message import EmailMessage
import smtplib
import ssl

email_sender = 'shptelemetry@gmail.com'
email_password = 'kfwo agdx hujr anrj'
email_reciever = '21bloggie@shiplake.org.uk'


def send_email(file_data, file_name, user_name):
    subject = 'Telemetry Post'
    
    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = email_reciever
    msg['Subject'] = subject
    msg.set_content(f'A new telemetry file has been uploaded\nPosted by: {user_name}\nFile Name: {file_name}')

    msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, msg.as_string())

