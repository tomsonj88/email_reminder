import logging
import smtplib
from email.message import EmailMessage
from os import getenv
from string import Template

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)


class Mail:
    def __init__(self, sender, recipient, message=None):
        self.sender = sender
        self.recipient = recipient
        self.message = message


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

    def send_email_to_book_debtor(self, database_data):
        from_address = getenv("EMAIL")
        for element in range(len(database_data)):
            to_address = database_data[element][1]
            name = database_data[element][2]
            book = database_data[element][3]
            return_date = database_data[element][4]
            msg = create_message(from_address, to_address, name, book,
                                 return_date)
            mail = Mail(from_address, to_address, msg)
            try:
                self.send(mail)
                logging.info(f"Email to {name} has been sent")
            except TimeoutError:
                logging.error(f"TimeoutError! Email to {name} has not been "
                              f"sent"
                              )
            except smtplib.SMTPDataError:
                logging.error(f"The SMTP server refused to accept the message "
                              f"data. Email to {name} has not been sent")


def create_message(from_address, to_address, name, book, return_date):
    message_template = Template("Hi $name.\n I lent you book: $book. "
                                "You promise me to return it till "
                                "$return_date. Please return it.\nBR\n"
                                )
    message = message_template.substitute(name=name,
                                          book=book,
                                          return_date=return_date
                                          )
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Please return my book "
    msg["From"] = from_address
    msg["To"] = to_address
    return msg.as_string()
