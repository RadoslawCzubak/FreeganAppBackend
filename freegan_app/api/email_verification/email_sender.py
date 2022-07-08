import smtplib

from email.message import EmailMessage

from dotenv import dotenv_values

env_config = dotenv_values('freegan_app/.env')


def send_verification_email(receiver_email: str, code: str):
    msg = EmailMessage()

    msg['Subject'] = f'Freegan App: email verification'
    msg['From'] = env_config["EMAIL"]
    msg['To'] = receiver_email

    msg.set_content(f"""
    Twój kod weryfikacyjny to: 
    {code}
    """)

    s = smtplib.SMTP_SSL(env_config["SMTP_ADDRESS"], int(env_config["SMTP_PORT"]))
    s.ehlo()
    s.login(env_config["EMAIL"], env_config["EMAIL_PASS"])
    s.send_message(msg)
    s.close()
