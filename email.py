# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
#with open(textfile) as fp:
    # Create a text/plain message
msg = MIMEText('TEST')

me == 'andrius-smth@yandex.ru'
you == 'andrius.momzyakov@gmail.com'
msg['Subject'] = 'test'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()