#with open('C:/Users/Rin/Desktop/water level monitoring system password.txt') as file:
#    email_password = file.read()

import smtplib
import ssl
from random import randint
import email.message
from Input_Validation import validate_email

def send_email_code(receiver_email, subject="CONFIRM EMAIL"):
    email_password = 'wnil kuoe tmgd bvxl'
    email_sender = 'ryllaneta@gmail.com' 

    code = randint(69696, 96969)

    if subject == "CONFIRM EMAIL":
        body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 20px;
                    }}
                    .container {{
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 20px;
                    }}
                    h2 {{
                        color: #333;
                    }}
                    p {{
                        color: #666;
                    }}
                    .code {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #007bff;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Water Level Monitoring System</h2>
                    <p>Dear User,</p>
                    <p>Your confirmation code for the water level monitoring system is:</p>
                    <p class="code">{code}</p>
                    <p>Please use this code to complete the verification process.</p>
                    <p>Thank you,</p>
                    <p>The Water Level Monitoring Team</p>
                </div>
            </body>
        </html>
        """
    else:
        body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 20px;
                    }}
                    .container {{
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 20px;
                    }}
                    h2 {{
                        color: #333;
                    }}
                    p {{
                        color: #666;
                    }}
                    .code {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #007bff;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Water Level Monitoring System</h2>
                    <p>Dear User,</p>
                    <p>Your verification code for the water level monitoring system is:</p>
                    <p class="code">{code}</p>
                    <p>Please use this code to complete the password reset process.</p>
                    <p>Thank you,</p>
                    <p>The Water Level Monitoring Team</p>
                </div>
            </body>
        </html>
        """
    
    Email_Object = email.message.EmailMessage()
    Email_Object['From'] = email_sender
    Email_Object['To'] = receiver_email
    Email_Object['Subject'] = subject
    Email_Object.add_alternative(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver_email, Email_Object.as_string())
    
    return str(code) # RETURN THE CODE


def email_validation(email):
    return validate_email(email)

if __name__== '__main__':
    input_email = input("Enter Your Valid Email: ")
    send_email_code(input_email)
