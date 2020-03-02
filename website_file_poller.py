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
import json
import requests
from bs4 import BeautifulSoup
import io
from PyPDF2 import PdfFileReader
import time
import smtplib

##################################################################################################################

# Login information
payload = {"username": "email@gmail.com", "password": "mypassword123"}

# E-mail information
user = "bot_email@gmail.com"        # from address
pwd = "botpassword123"              # from password
to = "receiver_email@gmail.com"     # to address

# Name to check
name = "name_to_check"

# Polling time
interval = 60 * 5                   # 5 minutes

##################################################################################################################

# URLs
loginURL = "http://this_is_a_website.com/login/index.php"
logoutURL = "http://this_is_a_website.com/login/logout.php"
scheduleURL = "http://page_with_files.com/"

# Sections to look for files
days = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SABADO", "DOMINGO"]

# Filename of previously checked files
filename = "path/to/program/folder/"+"checked.json"


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
            docs.append({"name": text, "url": link})

    return docs


def load_from_file():
    my_file = Path(filename)
    if my_file.exists():
        with open(filename, 'r') as f:
            try:
                previous = json.load(f)
            except:
                return []
            return previous
    else:
        return []


def save_to_file(docs):
    with open(filename, 'w') as f:
        docs_json = json.dump(docs, f)


def check_for_flights(docs, previous_dates):
    message = ""
    new = False     # flag to check if there are new files
    for doc in docs:
        # If file is new
        if doc['name'] not in previous_dates:
            new = True

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
                # Add file information to e-mail message
                message += doc['name'] + '\t' + doc['url'] + "\n"

    return new, message


def send_message(message):
    if message == "":
        subject = "NOTHING"
    else:
        subject = "SOMETHING!"
    
    sent = False
    while not sent:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            
            server.sendmail(
                user,
                to,
                f"Subject: {subject}\n\nLinks:\n{message}",
            )

            server.quit()
            sent = True
        # Error sending e-mail. Try again.
        except Exception as email_exception:
            print(email_exception, flush=True)
            time.sleep(1)       # sleep for 1 second

    print("SENT!", flush=True)
    #print(f"Subject: {subject}\n\nLinks:\n{message}", flush=True)


if __name__ == '__main__':
    previous = load_from_file()
    print("previous", previous, flush=True)

    while True:
        try:
            # Load previous checked files, so that it doesn't send repeated e-mails
            previous_dates = [doc['name'] for doc in previous]

            with requests.Session() as session:
                #Login the page
                login()

                # Get list of files
                docs = get_dictionary_files()

                # Check if there are new flights and if it contains the defined name
                new, message = check_for_flights(docs, previous_dates)

                # Logout from the page
                logout()

                # If there are new files, send an e-mail
                if new:
                    send_message(message)

                    # Save checked files to avoid repetitions
                    save_to_file(docs)
                    previous = docs
                    print("docs", docs, flush=True)

            # Sleep for 5 minutes
            time.sleep(interval)

        except Exception as e:
            print(e, flush=True)
            time.sleep(1)       # sleep for 1 second
