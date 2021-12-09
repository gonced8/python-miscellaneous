import requests
import smtplib
import ssl
import time


def send_email(email):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "from@gmail.com"
    receiver_email = email
    password = "password"
    message = f"""From: {sender_email}
To: {receiver_email}
Subject: Vacina

https://covid19.min-saude.pt/pedido-de-agendamento"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
    url = "https://covid19.min-saude.pt/pedido-de-agendamento"

    while True:
        r = requests.get(url)

        if not r.ok:
            print(f"HTTP request error. Status code: {r.status_code}. Esperar 1 min.")
        elif "Tem 23" not in r.text:
            send_email("to@gmail.com")
            print("VACINA")
            break
        else:
            print("Ainda não. Esperar 1 min.")

        time.sleep(60)
