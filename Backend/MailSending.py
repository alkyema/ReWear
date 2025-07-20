import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv
dotenv.load_dotenv()
import os

otp = 0

# Function to generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

# Function to send an email containing the OTP
def send_otp_email(to_email, otp):
    # print("Sending OTP to:", to_email)
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("senderEmail")
    sender_password = os.getenv("EmailPassword")  # Use an app password, not your Gmail password
    # print("Sender Email:", sender_password)
    # Email content
    subject = "Verify Your Smart Home Account: OTP Inside"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333333; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #2E86C1;">Welcome to Your Smart Home!</h2>
            <p>Dear Valued Customer,</p>
            <p>Thank you for choosing our smart home automation services. To ensure the security of your home and devices, please verify your account with the following One-Time Password (OTP):</p>
            <p style="font-size: 24px; color: #E74C3C; text-align: center;"><strong>{otp}</strong></p>
            <p>This OTP is valid for the next 10 minutes. Please enter it in the app to complete your verification.</p>
            <p>If you did not request this code, please secure your account by changing your password immediately and contacting our support team.</p>
            <p>Stay secure, stay smart!</p>
            <br>
            <p>Best Regards,</p>
            <p><strong>Your Smart Home Automation Team</strong></p>
            <p style="font-size: 12px; color: #999999;">If you have any questions or need further assistance, please do not hesitate to contact us at support@smarthome.com.</p>
        </div>
    </body>
    </html>
    """

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach the body as HTML
    message.attach(MIMEText(body, "html"))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS for security
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())
        return ("OTP sent successfully!")
    except Exception as e:
        return f"Failed to send OTP: {e}"
    finally:
        server.quit()

def verifyOTP(GivenOTP):
    if str(otp) == GivenOTP:
        return True
    else:
        return False

# Example usage
def GenerateMail(to_email):
    global otp
    # to_email = "alkyema4@gmail.com"
    otp = generate_otp()
    print(send_otp_email(to_email, otp))
    return otp
