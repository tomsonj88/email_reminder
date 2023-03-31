"""
E-MAIL REMINDER - RETURN MY BOOK
"""
import logging
from os import getenv
import sqlite3

from dotenv import load_dotenv  # pip install python-dotenv

from mail import MailBox
import database
from my_db_context_manager import MyDatabaseContextManager


logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    level=logging.INFO)


if __name__ == "__main__":
    load_dotenv()
    mailbox = MailBox(getenv("EMAIL"),
                      getenv("PASSWORD"),
                      getenv("SMTP_SERVER"),
                      getenv("PORT")
                      )
    connection = sqlite3.connect("database.db")
    with MyDatabaseContextManager(connection) as connector:
        book_debtor_data = database.show_who_didnt_return_book(connection, "books")
        mailbox.send_reminder(
            database.show_rows_x_days_before_return(connection, "books"))
    mailbox.send_email_for_return_book(book_debtor_data)
    logging.info("DONE")
