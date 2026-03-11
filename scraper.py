import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

SAPO_URL = "https://www.sapo.pt/"

def get_featured_news():
    response = requests.get(SAPO_URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # A notícia destacada aparece logo abaixo das capas dos jornais
    article = soup.select_one("article")

    if not article:
        return None, None

    title = article.get_text(strip=True)
    link = article.find("a")["href"]

    # Garantir link absoluto
    if link.startswith("/"):
        link = "https://www.sapo.pt" + link

    return title, link


def send_email(subject, body):
    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]
    recipient = os.environ["EMAIL_TO"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)


def main():
    title, link = get_featured_news()

    if not title:
        send_email("SAPO – Falha ao obter notícia", "Não foi possível obter a notícia destacada.")
        return

    body = f"Título: {title}\nLink: {link}"
    send_email("Notícia destacada do SAPO", body)


if __name__ == "__main__":
    main()
