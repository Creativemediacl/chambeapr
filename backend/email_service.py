import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(to_email: str, subject: str, html: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"ChambeaPR <{GMAIL_USER}>"
        msg["To"] = to_email
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_welcome_email(to_email: str, full_name: str, trial_days: int = 30):
    html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f0f2f5;padding:20px;"><div style="background:linear-gradient(135deg,#1B2A4A,#2C3E6B);padding:30px;text-align:center;border-radius:12px 12px 0 0;"><h1 style="color:#F5A623;margin:0;">ChambeaPR</h1></div><div style="background:white;padding:30px;border-radius:0 0 12px 12px;"><h2 style="color:#1B2A4A;">Bienvenido, {full_name}!</h2><p style="color:#444;line-height:1.6;">Tu perfil ha sido creado. Tu periodo de prueba de <strong style="color:#F5A623;">{trial_days} dias</strong> ha comenzado.</p><a href="https://chambeapr.com/dashboard" style="display:block;background:#F5A623;color:#1B2A4A;text-decoration:none;padding:15px;text-align:center;border-radius:10px;font-weight:bold;margin:20px 0;">Ver Mi Perfil</a><p style="color:#666;font-size:0.85em;">Preguntas? chambeaproficial@gmail.com</p></div></div>"""
    return send_email(to_email, "Bienvenido a ChambeaPR!", html)

def send_trial_ending_email(to_email: str, full_name: str, days_left: int):
    html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;"><div style="background:#1B2A4A;padding:30px;text-align:center;"><h1 style="color:#F5A623;">ChambeaPR</h1></div><div style="background:white;padding:30px;"><h2 style="color:#1B2A4A;">Hola {full_name},</h2><p>Tu prueba termina en <strong style="color:#c1121f;">{days_left} dias</strong>.</p><a href="https://chambeapr.com/subscribe" style="display:block;background:#F5A623;color:#1B2A4A;text-decoration:none;padding:15px;text-align:center;border-radius:10px;font-weight:bold;margin:20px 0;">Suscribirme - $9.99/mes</a></div></div>"""
    return send_email(to_email, f"Tu prueba termina en {days_left} dias - ChambeaPR", html)

def send_password_reset_email(to_email: str, full_name: str, reset_token: str):
    html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;"><div style="background:#1B2A4A;padding:30px;text-align:center;"><h1 style="color:#F5A623;">ChambeaPR</h1></div><div style="background:white;padding:30px;"><h2 style="color:#1B2A4A;">Hola {full_name},</h2><p>Haz clic para restablecer tu contrasena:</p><a href="https://chambeapr.com/reset-password?token={reset_token}" style="display:block;background:#F5A623;color:#1B2A4A;text-decoration:none;padding:15px;text-align:center;border-radius:10px;font-weight:bold;margin:20px 0;">Restablecer Contrasena</a><p style="color:#666;font-size:0.85em;">Este enlace expira en 1 hora.</p></div></div>"""
    return send_email(to_email, "Restablecer tu contrasena - ChambeaPR", html)
