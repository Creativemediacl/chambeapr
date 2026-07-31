import resend
import os
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

def send_welcome_email(to_email: str, full_name: str, trial_days: int = 30):
    try:
        resend.Emails.send({
            "from": "ChambeaPR <onboarding@resend.dev>",
            "to": to_email,
            "subject": "Bienvenido a ChambeaPR! Tu periodo gratis ha comenzado",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f0f2f5;padding:20px;"><div style="background:linear-gradient(135deg,#1B2A4A,#2C3E6B);padding:30px;text-align:center;border-radius:12px 12px 0 0;"><h1 style="color:#F5A623;margin:0;">ChambeaPR</h1><p style="color:#ccd6f6;margin-top:5px;">Conectando Puerto Rico</p></div><div style="background:white;padding:30px;border-radius:0 0 12px 12px;"><h2 style="color:#1B2A4A;">Bienvenido, {full_name}!</h2><p style="color:#444;line-height:1.6;">Tu perfil en ChambeaPR ha sido creado exitosamente. Tu periodo de prueba gratuita de <strong style="color:#F5A623;">{trial_days} dias</strong> ha comenzado.</p><div style="background:#fff3cd;border:2px solid #F5A623;border-radius:10px;padding:15px;margin:20px 0;text-align:center;"><h3 style="color:#1B2A4A;margin:0 0 5px 0;">Tu prueba termina en {trial_days} dias</h3><p style="color:#555;margin:0;font-size:0.9em;">Despues solo $9.99/mes para mantener tu perfil activo</p></div><a href="https://chambeapr.com" style="display:block;background:#F5A623;color:#1B2A4A;text-decoration:none;padding:15px;text-align:center;border-radius:10px;font-weight:bold;font-size:1.1em;">Ver Mi Perfil en ChambeaPR</a><p style="color:#666;font-size:0.85em;margin-top:20px;">Si tienes preguntas contactanos en chambeaproficial@gmail.com</p></div></div>"""
        })
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_trial_ending_email(to_email: str, full_name: str, days_left: int):
    try:
        resend.Emails.send({
            "from": "ChambeaPR <onboarding@resend.dev>",
            "to": to_email,
            "subject": f"Tu periodo gratis termina en {days_left} dias - ChambeaPR",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f0f2f5;padding:20px;"><div style="background:linear-gradient(135deg,#1B2A4A,#2C3E6B);padding:30px;text-align:center;border-radius:12px 12px 0 0;"><h1 style="color:#F5A623;margin:0;">ChambeaPR</h1></div><div style="background:white;padding:30px;border-radius:0 0 12px 12px;"><h2 style="color:#1B2A4A;">Hola {full_name},</h2><p style="color:#444;line-height:1.6;">Tu periodo de prueba gratuita termina en <strong style="color:#c1121f;">{days_left} dias</strong>.</p><p style="color:#444;">Para mantener tu perfil activo y seguir recibiendo clientes, suscribete por solo $9.99/mes.</p><a href="https://chambeapr.com/subscribe" style="display:block;background:#F5A623;color:#1B2A4A;text-decoration:none;padding:15px;text-align:center;border-radius:10px;font-weight:bold;font-size:1.1em;margin:20px 0;">Suscribirme Ahora - $9.99/mes</a><p style="color:#666;font-size:0.85em;">Preguntas? chambeaproficial@gmail.com</p></div></div>"""
        })
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_password_reset_email(to_email: str, full_name: str, reset_token: str):
    try:
        resend.Emails.send({
            "from": "ChambeaPR <onboarding@resend.dev>",
            "to": to_email,
            "subject": "Restablecer tu contrasena - ChambeaPR",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f0f2f5;padding:20px;"><div style="background:linear-gradient(135deg,#1B2A4A,#2C3E6B);padding:30px;text-align:center;border-radius:12px 12px 0 0;"><h1 style="color:#F5A623;margin:0;">ChambeaPR</h1></div><div style="background:white;padding:30px;border-radius:0 0 12px 12px;"><h2 style="color:#1B2A4A;">Hola {full_name},</h2><p style="color:#444;">Recibimos una solicitud para restablecer tu contrasena.</p><a href="https://chambeapr.com/reset-password?token={reset_token}" style="display:block;background:#F5A623;color:#1B2A4A;text-decoration:none;padding:15px;text-align:center;border-radius:10px;font-weight:bold;font-size:1.1em;margin:20px 0;">Restablecer Contrasena</a><p style="color:#666;font-size:0.85em;">Si no solicitaste esto ignora este email. El enlace expira en 1 hora.</p></div></div>"""
        })
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
