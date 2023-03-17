import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64

class Mail:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            print("Missing Google login credentials")
            quit()
        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
        except:
            print("gmail error")
            quit()

    def send(self,to,subject,messageList):
        try:
            message = EmailMessage()

            messagetxt = ""
            for row in messageList:
                messagetxt = "\n".join([messagetxt, row])
            message.set_content(messagetxt)

            message['To'] = to
            message['From'] = 'aswepda@gmail.com'
            message['Subject'] = subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {'raw': encoded_message}
            send_message = (self.service.users().messages().send(userId="me", body=create_message).execute())
        except:
            print("gmail error")