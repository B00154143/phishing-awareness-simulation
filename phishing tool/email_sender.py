import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Gmail SMTP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# In-memory log (used for dashboard later)
email_logs = []


def send_email(to_email, subject, body, mode="auto"):
    

    from_email = "sofimeilally03@gmail.com"
    password = "your_app_password"

    # Save log entry
    log_entry = {
        "to": to_email,
        "subject": subject,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "",
        "mode": mode
    }

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        # Try REAL email sending
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(from_email, password)
            server.send_message(msg)

        log_entry["status"] = "sent (real email)"
        email_logs.append(log_entry)

        print(f" Email sent successfully to {to_email}")

        return True

    except Exception as e:
        # Fallback: simulation mode (VERY IMPORTANT FOR YOUR PROJECT)
        log_entry["status"] = f"simulated (failed real send: {str(e)})"
        email_logs.append(log_entry)

        print(f" Email NOT sent. Running in simulation mode for {to_email}")
        print("Reason:", e)

        print(" Simulated Email Content:")
        print("To:", to_email)
        print("Subject:", subject)
        print("Body:", body)

        return False