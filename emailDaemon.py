import getpass
import smtplib
from email.mime.text import MIMEText

class emailer():
    """Class to send text as email to the specified recipient. For security,
    the email credentials are prompted from the user at explicit function
    call, as is the sending of the email. Can be configured to be interactive,
    which would allow the user to provide the recipient with the send function
    call. Additionally, a recipient email can be requested using either
    initialization, using explicit function call or, depending on the
    interaction level, fed during the send function call."""

    def __init__(self, subject=None, body=None, interactive=0, recipient=None):
        """Initializer"""
        self.interactive = interactive
        self.recipient = recipient
        self.email = None
        self.password = None
        self.body = body
        self.subject = subject

    def setUpCredentials(self):
        """Get email creds for sender"""
        self.email = input("Enter your email: ")
        self.password = getpass.getpass()

    def setUpRecipient(self):
        num = int(input("Enter the total number of recipients: "))
        recipients = []
        for i in range(num):
            recipient.append(input("Enter recipient number %s:" % (i+1)))
        self.recipient = recipient

    def sendEmail(self, body=None, subject=None, recipients=None):
        if recipient is None:
            if isinstance(self.recipient, str):
                if body is not None:
                    msg = MIMEText(body)
                    msg
                    if subject is None:
                        msg['Subject'] = self.subject
                        


