import logging
import smtplib
from email.message import EmailMessage
from os import getenv
from string import Template

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)


class Mail:
    def __init__(self, sender, recipient, msg="", subject=""):
        self.sender = sender
        self.recipient = recipient
        self.message = self.create_message(msg, subject)

    def create_message(self, text, subject):
        msg = EmailMessage()
        msg.set_content(text)
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = self.recipient
        return msg.as_string()


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

    def send_email_for_return_book(self, database_data):
        from_address = getenv("EMAIL")
        subject = "Return my book"
        for element in range(len(database_data)):
            to_address, name, book, return_date = prepare_db_data(
                database_data, element)
            msg_template = Template("Hi $name.\n I lent you book: $book. "
                                    "You promise me to return it till "
                                    "$return_date. Please return it.\nBR\n")
            message = msg_template.substitute(name=name,
                                              book=book,
                                              return_date=return_date
                                              )
            mail = Mail(from_address, to_address, message, subject)

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

    def send_reminder(self, database_data):
        from_address = getenv("EMAIL")
        subject = "Reminder"
        for element in range(len(database_data)):
            to_address, name, book, return_date = prepare_db_data(
                database_data, element)

            msg_template = Template("Hi $name, please remember, that in $days "
                                    "days ($return_date) you will have to "
                                    "return my book $book.")
            message = msg_template.substitute(name=name,
                                              book=book,
                                              return_date=return_date,
                                              days=getenv("REMINDER")
                                              )
            mail = Mail(from_address, to_address, message, subject)
            self.send(mail)
            logging.info(f"Reminder to {name} has been sent")


def prepare_db_data(db_data, index):
    to_address = db_data[index][1]
    name = db_data[index][2]
    book = db_data[index][3]
    return_date = db_data[index][4]
    return to_address, name, book, return_date
