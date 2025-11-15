import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

def send_contact_notification(contact_data):
    """Send email notification for new contact message"""
    try:
        # Email configuration
        smtp_server = config('EMAIL_HOST', default='smtp.gmail.com')
        smtp_port = config('EMAIL_PORT', default=587, cast=int)
        email_user = config('EMAIL_USER')
        email_password = config('EMAIL_PASSWORD')
        admin_email = config('ADMIN_EMAIL', 'viyl@kionehardware.co.ke')

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = admin_email
        msg['Subject'] = f"New Contact Message: {contact_data['subject']}"

        # Email body
        body = f"""
        <h2>New Contact Message Received</h2>
        <p><strong>Name:</strong> {contact_data['name']}</p>
        <p><strong>Email:</strong> {contact_data['email']}</p>
        <p><strong>Phone:</strong> {contact_data.get('phone', 'Not provided')}</p>
        <p><strong>Subject:</strong> {contact_data['subject']}</p>
        <p><strong>Message:</strong></p>
        <p>{contact_data['message']}</p>
        <hr>
        <p>This message was sent from the Kione Hardware website contact form.</p>
        """

        msg.attach(MIMEText(body, 'html'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False