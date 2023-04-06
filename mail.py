"""
Module mail.py contains classes and methods for handling emails
"""

import logging
import smtplib
from email.message import EmailMessage
from os import getenv
from string import Template

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)


class Mail:# pylint: disable=too-few-public-methods
    """
    Class Mail handles creation of email messages
    """
    def __init__(self,
                 sender: str,
                 recipient: str,
                 msg: str = "",
                 subject: str = ""
                 ):
        self.sender = sender
        self.recipient = recipient
        self.message = self.create_message(msg, subject)

    def create_message(self, text: str, subject: str) -> str:
        """
        Method for create proper structure of email message using
        EmailMessage class (included in python libs)
        :param text: string with email content
        :param subject: subject of email
        :return: string with email message
        """
        msg = EmailMessage()
        msg.set_content(text)
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = self.recipient
        return msg.as_string()


class MailBox:
    """
    Class MailBox contain methods for login to mailbox and for sending
    emails. Class have also procedure to send reminder and
    send request to return book.
    """
    def __init__(self,
                 username: str,
                 password: str,
                 smtp_server: str,
                 ssl_enable: bool = False,
                 port: int = 465,
                 mails: list[str] = None
                 ): #pylint: disable=(too-many-arguments
        self.username = username
        self.password = password
        self.smtp_server = smtp_server
        self.port = port
        self.ssl_enable = ssl_enable
        self.mails = mails

    def send(self, mail):
        """
        Method handles email sending
        :param mail: email in structured form from EmailMessage str
        """
        if not self.ssl_enable:
            connection = smtplib.SMTP(self.smtp_server, self.port)
        else:
            connection = smtplib.SMTP_SSL(self.smtp_server, self.port)
        with connection as server:
            self.login(server)
            server.sendmail(mail.sender, mail.recipient, mail.message)

    def login(self, server_obj):
        """
        Method for log in into email box
        :param server_obj:
        :return: None
        """
        server_obj.login(self.username, self.password)

    def send_email_for_return_book(self, database_data):
        """
        Method sending email to people how didn't return the book
        :param database_data:
        :return:
        """
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
                logging.info("Email to %s has been sent", name)
            except TimeoutError:
                logging.error("TimeoutError! Email to %s has not been "
                              "sent", name
                              )
            except smtplib.SMTPDataError:
                logging.error("The SMTP server refused to accept the message "
                              "data. Email to %s has not been sent", name
                              )

    def send_reminder(self, database_data) -> None:
        """
        Method sends reminder to person who have to return book within
        specified number of days. Number of days is specified in variable
        EMAIL in .env file.
        """
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
            logging.info("Reminder to %s has been sent", name)


def prepare_db_data(db_data, index):
    """
    Function obtain destination address, name, book, return date from
    database and returns them in order: to_address, name, book,
    return date
    """
    to_address = db_data[index][1]
    name = db_data[index][2]
    book = db_data[index][3]
    return_date = db_data[index][4]
    return to_address, name, book, return_date
