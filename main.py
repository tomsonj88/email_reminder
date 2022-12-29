"""
E-MAIL REMINDER - RETURN MY BOOK
"""
import logging
from os import getenv

from dotenv import load_dotenv  # pip install python-dotenv

from mail import MailBox
from database import Database


logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    level=logging.INFO)


if __name__ == "__main__":
    load_dotenv()
    mailbox = MailBox(getenv("EMAIL"),
                      getenv("PASSWORD"),
                      getenv("SMTP_SERVER"),
                      getenv("PORT")
                      )
    db = Database("database.db")
    book_debtor_data = db.show_who_didnt_return_book("books")
    mailbox.send_email_for_return_book(book_debtor_data)
    logging.info("DONE")

    print(db.show_rows_6_days_before_return("books"))
    mailbox.send_remainder(db.show_rows_6_days_before_return("books"))
