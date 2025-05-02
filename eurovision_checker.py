import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import os

# Config à récupérer depuis Render (via variables d'environnement)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Fonction d'envoi d'email
def send_email():
    subject = "🎫 Billets Eurovision 17 mai disponibles !"
    body = "Des billets sont apparus sur fansale.ch : https://www.fansale.ch/fansale/tickets/search?query=eurovision"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("📧 Email envoyé !")
    except Exception as e:
        print(f"Erreur envoi email : {e}")

# Configuration de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver_path = "/usr/bin/chromedriver"
url = "https://www.fansale.ch/fansale/tickets/search?query=eurovision"

def check_for_tickets():
    try:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(5)
        page_text = driver.page_source.lower()
        if "17 mai" in page_text or "17.05" in page_text:
            print("🎉 Billets trouvés !")
            send_email()
        else:
            print("🔍 Aucun billet pour le 17 mai.")
    except Exception as e:
        print(f"Erreur vérification : {e}")
    finally:
        driver.quit()

check_for_tickets()
