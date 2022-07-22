import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

class Mail:
    def __init__(self, id, pw):
        self.sender_address = id
        self.sender_pass = pw
        
    def send(self, receiver_address, subject, mail_content, filePaths):
        message = MIMEMultipart()
        message['From'] = self.sender_address
        message['To'] = receiver_address
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'plain'))
        
        for filePath in filePaths:
            part = MIMEBase('application', "octet-stream")
            with open(filePath, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(Path(filePath).name))
            message.attach(part)
        
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(self.sender_address, self.sender_pass)
        text = message.as_string()
        session.sendmail(self.sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')