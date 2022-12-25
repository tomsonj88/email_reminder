"""
Tests for mail.py module
"""
from os import getenv

from dotenv import load_dotenv
from unittest.mock import patch

from mail import Mail, MailBox

load_dotenv()


@patch("smtplib.SMTP_SSL")
def test_mail_sending(mock_smtp):
    mail = Mail(getenv("EMAIL"),
                getenv("EMAIL"),
                f'From:{getenv("EMAIL")}\n \nHello')
    mailbox = MailBox(getenv("EMAIL"),
                      getenv("PASSWORD"),
                      getenv("SMTP_SERVER"),
                      getenv("PORT")
                      )
    mailbox.send(mail)
    mock_smtp.assert_called()
    context = mock_smtp.return_value.__enter__.return_value
    context.sendmail.assert_called_with(getenv("EMAIL"),
                                        getenv("EMAIL"),
                                        f'From:{getenv("EMAIL")}\n \nHello')
