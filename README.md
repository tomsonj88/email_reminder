"# email_reminder" 
# "Return my book! - e-mail reminder"

### Simply library to send e-mail reminder to people, who forgot return our book.
### Project was created in Python and database in SQL Lite.

## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is to send e-mail reminder for book return. Two main features are:
- send reminder before book return date
- send reminder after book return date

These two features contains different email templates.

Data about people who lend books are stored in SQL Lite database. 

Project contain module with class Mail (create mails using EmailMessage class), 
Mailbox (can login to mailbox, send an e-mail, send reminders). 
Class Database allows to create table, add, delete rows, show all rows).
Project have logger with main events and with SQL query events (print every
executed SQL query)

## Technologies
Python, SQL

## Setup

At the beginning install python-dotenv using command: 
"pip install python-dotenv"

Create and fill .env file based on .env.dist. Put the file
to the project catalog.

You can use database:
 1) from repository (Remember to change destination email
 in database, because reminder will be send to test emails
 and you won't see any effect)
 2) create your own database - do it manually (you can base on
 db from repository) or use functions from database.py:
 create_table, add_row
 
 Execute main.py

 





    
