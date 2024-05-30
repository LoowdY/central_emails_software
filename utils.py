import ssl
import smtplib
from email.message import EmailMessage

#rdga slmm ojns ztum

def enviar_email(usuario_email, destinatario, titulo, corpo, senha_aplicativo):
    mensagem = EmailMessage()
    mensagem['From'] = usuario_email
    mensagem['To'] = destinatario
    mensagem['Subject'] = titulo
    mensagem.set_content(corpo)
    safe = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as smtp:
        smtp.login(usuario_email, senha_aplicativo)
        smtp.sendmail(usuario_email, destinatario,mensagem.as_string())


