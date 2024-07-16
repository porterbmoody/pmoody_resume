#%%
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

from_email = 'porterbmoody@gmail.com'
email_password = 'pxxo ntgk qqho ikpf'
smtp_server = 'smtp.gmail.com'
smtp_port = 587

subject = "Test"
body = """
Dear Chris,

This is Porter with Number One Marketing Company. Do you want to increase your ad revenue by 3x-5x?
If so we have the program for you. 

Best regards,
Porter
"""
body

#%%
to_emails = ['portermoodymusic@gmail.com', ]

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, email_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

for to_email in to_emails:
    send_email(to_email, subject, body)
    time.sleep(1)


#%%

