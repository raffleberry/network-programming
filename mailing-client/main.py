import smtplib
from sys import exit
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# establish connection to server
# turn on `lesssecureapps` in the following link(for gmail)
# https://myaccount.google.com/lesssecureapps
server = smtplib.SMTP('smtp.gmail.com', 25)

server.ehlo()

# required for gmail
server.starttls()

try:
  with open("credentials.txt", "r") as f:
    user, password = f.readlines()
except FileNotFoundError as f:
  print("File `credentials.txt` not found, please store your email and password in that file like this:\n<username>\n<password>")
  exit(1)

server.login(user=user, password=password)

msg = MIMEMultipart()
# extends the format of email messages to support text in character sets other than ASCII,
# as well as attachments of audio, video, images, and application programs.

msg['From'] = "Debadutta Padhial"
msg['To'] = "raffleberry42@gmail.com"
msg['Subject'] = "Yo"

try:
  with open("message.txt", "r") as f:
    message = f.read()
except FileNotFoundError as f:
  print("File `message.txt` not found, please store your email contents in that file")
  exit(1)

msg.attach(MIMEText(message, "plain"))

avatar = 'avatar.jpg'
attachment = open(avatar, "rb").read() # read binary
payload = MIMEBase('application', 'octet-stream')
payload.set_payload(attachment)

payload.add_header('Content-Disposition', f'attachment', filename=avatar)
encoders.encode_base64(payload)

msg.attach(payload)

text = msg.as_string()

# send mail
server.sendmail(user, 'raffleberry42@gmail.com', text)

exit(0)