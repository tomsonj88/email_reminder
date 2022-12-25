"""
E-MAIL REMINDER - RETURN MY BOOK
"""
import logging
import smtplib
from dotenv import \
    load_dotenv  # trzeba było doinstalować: pip install python-dotenv
from email.message import EmailMessage
from os import getenv
from string import Template

from mail import Mail, MailBox
from database import Database

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    level=logging.INFO)


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


def send_email_to_book_debtor(database_data):
    from_address = getenv("EMAIL")
    for element in range(len(database_data)):
        to_address = database_data[element][1]
        name = database_data[element][2]
        book = database_data[element][3]
        return_date = database_data[element][4]
        msg = create_message(from_address, to_address, name, book, return_date)
        mail = Mail(from_address, to_address, msg)
        try:
            mailbox.send(mail)
            logging.info(f"Email to {name} has been sent")
        except TimeoutError:
            logging.error(f"TimeoutError! Email to {name} has not been "
                          f"sent"
                          )
        except smtplib.SMTPDataError:
            logging.error(f"The SMTP server refused to accept the message "
                          f"data. Email to {name} has not been sent")


if __name__ == "__main__":
    load_dotenv()
    mailbox = MailBox(getenv("EMAIL"),
                      getenv("PASSWORD"),
                      getenv("SMTP_SERVER"),
                      getenv("PORT")
                      )
    db = Database("database.db")
    book_debtor_data = db.show_who_didnt_return_book("books")
    send_email_to_book_debtor(book_debtor_data)
    logging.info("DONE")
