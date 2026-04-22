import imaplib
import email
import requests
import time
from twocaptcha import TwoCaptcha

# Initialize variables
EMAIL_USER = 'your_email@gmail.com'
EMAIL_PASS = 'your_email_password'
TWO_CAPTCHA_API_KEY = 'your_2captcha_api_key'
SPEECH_API_URL = 'https://selsi.io/api/v1/signup' # Example URL for signup API

def retrieve_otp():
    # Connect to Gmail IMAP
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select('inbox')

    # Search for the latest email containing the OTP
    result, data = mail.search(None, 'ALL')
    if result == 'OK':
        latest_email_id = data[0].split()[-1]
        result, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # Assuming the OTP is in the email body
        otp = extract_otp(msg)
    else:
        print('No emails found.')
        return None
    
    mail.logout()
    return otp

def extract_otp(msg):
    # Extract and return OTP from the email message
    # This will depend on the format of the email 
    # Here's an example parsing logic:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                # Logic to extract OTP from body
                return body.split('Your OTP is:')[1].strip()  # Adapt as necessary
    return None

def solve_captcha():
    solver = TwoCaptcha(TWO_CAPTCHA_API_KEY)
    result = solver.recaptcha(sitekey='your_site_key', url='https://selsi.io/')
    return result['code']  # Retrieval of CAPTCHA solution

def signup_to_selsi():
    otp = retrieve_otp()
    if not otp:
        print("Failed to retrieve OTP.")
        return

    captcha_solution = solve_captcha()
    data = {
        'email': EMAIL_USER,
        'otp': otp,
        'captcha': captcha_solution,
        # Add other fields as required by the signup API
    }
    
    response = requests.post(SPEECH_API_URL, json=data)
    print(response.json())  # Handle response as needed

if __name__ == "__main__":
    signup_to_selsi()