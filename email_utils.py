from email.message import EmailMessage
import aiosmtplib
from fastapi.templating import Jinja2Templates

from config import settings

templates= Jinja2Templates(directory="templates")

# send email function
async def send_email(
    to_email: str,
    subject: str,
    plain_text: str,
    html_content: str| None = None,
)-> None:
    message=EmailMessage()
    message["From"]=settings.mail_from
    message["To"]=to_email
    message["Subject"]=subject
    message.set_content(plain_text)
    if html_content:
        message.add_alternative(html_content, subtype="html")
    
    await aiosmtplib.send(
        message,
        hostname=settings.mail_server,
        port=settings.mail_port,
        username=settings.mail_username if settings.mail_username else None,
        password=settings.mail_password.get_secret_value() or None,
        start_tls=settings.mail_use_tls,
    )

async def send_password_reset_email(to_email:str,username:str,token:str)-> None:
    reset_url=f"{settings.frontend_url}/reset-password?token={token}"
    subject="Password Reset Request"
    plain_text=f"Hello {username},\n\nYou requested a password reset. Click the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email."
    template = templates.get_template("email/password_reset.html")
    html_content=template.render(username=username,reset_url=reset_url)
    
    await send_email(to_email,subject,plain_text,html_content)
    