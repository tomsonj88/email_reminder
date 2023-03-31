"""
Tests for mail.py module
"""
from os import getenv
from email.message import EmailMessage
from unittest.mock import patch

from dotenv import load_dotenv

from mail import Mail, MailBox

load_dotenv()


@patch("smtplib.SMTP_SSL")
def test_mail_sending(mock_smtp):
    """
    Test checking if mail was sent. Test checks two cases:
    1) if SMTP_SSL was called
    2) if method for email sending and mock_smtp return the same value
    """
    mail = Mail(getenv("EMAIL"),
                getenv("EMAIL"),
                "Hello"
                )
    mailbox = MailBox(getenv("EMAIL"),
                      getenv("PASSWORD"),
                      getenv("SMTP_SERVER"),
                      getenv("PORT")
                      )
    mailbox.send(mail)
    mock_smtp.assert_called()
    context = mock_smtp.return_value.__enter__.return_value

    expected_mail = EmailMessage()
    expected_mail.set_content("Hello")
    expected_mail["Subject"] = ""
    expected_mail["From"] = getenv("EMAIL")
    expected_mail["To"] = getenv("EMAIL")
    context.sendmail.assert_called_with(
        expected_mail["From"],
        expected_mail["To"],
        expected_mail.as_string()
        )
