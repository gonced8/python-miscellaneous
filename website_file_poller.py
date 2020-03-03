#!~/env/bin/python3

'''
This script polls a website, which requires login, to check if there are new files.
If there are new files, it downloads them and checks if there is a match of a string in the files' contents.
If there were new files, it sends an e-mail to a user notifying him accordingly.

requirements:
    bs4
    requests
    PyPDF2

By: gonced8
'''
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import io
from PyPDF2 import PdfFileReader
import time
from email.mime.text import MIMEText
from email.header import Header
import smtplib

##################################################################################################################

# Login information
payload = {"username": "email@gmail.com", "password": "mypassword123"}

# E-mail information
sender = "bot_email@gmail.com"        # from address
pwd = "botpassword123"              # from password
to = "receiver_email@gmail.com"     # to address

# Name to check
name = "name_to_check"

# Polling time
interval = 60 * 5                   # 5 minutes
exception_interval = 1              # 1 second

##################################################################################################################

# URLs
loginURL = "http://this_is_a_website.com/login/index.php"
logoutURL = "http://this_is_a_website.com/login/logout.php"
scheduleURL = "http://page_with_files.com/"

# Sections to look for files
days = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SABADO", "DOMINGO"]

# Filename of previously checked files
filename = "path/to/program/folder/"+"checked.txt"


def login():
    response = session.post(loginURL, data=payload)
    print("login", response, flush=True)


def logout():
    response = session.get(logoutURL)
    print("logout", response, flush=True)


def get_dictionary_files():
    page_request = session.get(scheduleURL)  # get page of schedules
    schedules_page = page_request.content   # get page content

    soup = BeautifulSoup(schedules_page, "html.parser")
   
    docs = []

    # Loop through day sections
    for day in days:
        section = soup.find('li', attrs = {'aria-label': day})
        files = section.find_all('div', attrs = {'class': 'activityinstance'})

        # Make a list of dictionaries with keys: name and url
        for f in files:
            link = f.find('a').get('href')
            text = f.getText()
            text = text.rsplit(' ', 1)[0]
            docs.append({"name": text, "url": link, "day": day})

    return docs


def load_from_file():
    my_file = Path(filename)
    if my_file.exists():
        with open(filename, 'r') as f:
            try:
                previous = f.readlines()
                previous = [line.strip() for line in previous]
            except:
                return []
            return previous
    else:
        return []


def save_to_file(docs):
    docs_names = '\n'.join(docs)
    with open(filename, 'w') as f:
        f.write(docs_names)


def check_for_flights(docs, previous):
    new = []        # list of new docs
    for doc in docs:
        # If file is new
        if doc['name'] not in previous:
            new.append(doc)

            # Get correct PDF link
            con = session.get(doc['url'], allow_redirects=True)  # to get content after redirection
            pdf_url = con.url  # PDF link
            pdf = session.get(pdf_url)  # get PDF page

            # Open PDF
            pdf_file = io.BytesIO(pdf.content)  # PDF binary content
            reader = PdfFileReader(pdf_file)
            contents = reader.getPage(0).extractText()

            # Check if name is in the PDF
            if name.lower() in contents.lower():
                new[-1]["match"] = True
            else:
                new[-1]["match"] = False

    return new


def send_message(new):
    message = "Ficheiros novos:\n\n"
    match = False

    for doc in new:
        message += "[{}] - {} ({}) - {}\n".format(
                'X' if doc['match'] else ' ', doc['name'], doc['day'], doc['url'])

        if doc['match']:
            match = True

    if match:
        subject = "SOMETHING"
    else:
        subject = "NOT SOMETHING"

    email = MIMEText(message.encode('utf-8'), _charset='utf-8')
    email['Subject'] = Header(subject, "utf-8")
    email['From'] = sender
    email['To'] = to

    sent = False

    while not sent:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(sender, pwd)
            
            server.sendmail(sender, to, email.as_string())

            server.quit()
            sent = True
        # Error sending e-mail. Try again.
        except Exception as email_exception:
            print(email_exception, flush=True)
            time.sleep(exception_interval)       # sleep for 1 second

    print("SENT!", flush=True)
    print(email, flush=True)


if __name__ == '__main__':
    # Load previous checked files, so that it doesn't send repeated e-mails
    previous = load_from_file()
    print("previous", previous, flush=True)

    while True:
        try:
            with requests.Session() as session:
                #Login the page
                login()

                # Get list of files
                docs = get_dictionary_files()

                # Check if there are new flights and if it contains the defined name
                new = check_for_flights(docs, previous)
                print("new", new)

                # Logout from the page
                logout()

                # If there are new files, send an e-mail
                if new:
                    send_message(new)

                    # Save checked files to avoid repetitions
                    previous = [doc["name"] for doc in docs]
                    save_to_file(previous)
                    print("docs", previous, flush=True)

            # Sleep for 5 minutes
            time.sleep(interval)

        except Exception as e:
            print(e, flush=True)
            time.sleep(exception_interval)       # sleep for 1 second
