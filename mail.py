import smtplib
import ssl


class MailBox:
    def __init__(self,
                 username,
                 password,
                 smtp_server,
                 context,
                 port=465,
                 mails=None
                 ):
        self.username = username
        self.password = password
        self.smtp_server = smtp_server
        self.port = port
        self.context = context
        self.mails = mails

    def send(self, mail):
        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            self.login(server)
            server.sendmail(mail.sender, mail.recipient, mail.message)

    def login(self, server_obj):
        server_obj.login(self.username, self.password)


class Mail:
    def __init__(self, sender, recipient, message=None):
        self.sender = sender
        self.recipient = recipient
        self.message = message
