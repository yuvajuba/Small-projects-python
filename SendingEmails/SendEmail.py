import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

with open("ident.txt", "r") as f:
    lines = f.read().splitlines()
    sender = lines[0].strip()
    password = lines[1].strip()

html = Template(Path("index.html").read_text())
email = EmailMessage()

email["from"] = "A friend"
email["to"] = sender
email["subject"] = "IMPORTANT !!!"

email.set_content(html.substitute({"name": input("Name : ")}), "html")


with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender, password)
    smtp.send_message(email)

print("All good")
