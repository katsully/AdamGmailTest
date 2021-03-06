import httplib2
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import email.encoders
from pythonosc import osc_server
from pythonosc import dispatcher
import sys
import time
import subprocess
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client import client

import receive_emails

import logging
import gspread

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# silence ImportError: file_cache is unavailable when using oauth2client >= 4.0.0 or google-auth error
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CLIENT_SECRET_FILE = 'credentials_old.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-modify.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    creds = get_credentials()
    http = gspread.authorize(creds)
    service = build('gmail', 'v1', credentials=creds)
    if attachmentFile:
        message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
    else: 
        message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    result = SendMessageInternal(service, "sjd.9f8.auy@gmail.com", message1)
    return result

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    

def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}

def createMessageWithAttachment(
    sender, to, subject, msgHtml, msgPlain, attachmentFile):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      msgHtml: Html message to be sent
      msgPlain: Alternative plain text message for older email clients          
      attachmentFile: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['from'] = sender
    # set email address
    user_email = sender
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    messageR.attach(MIMEText(msgHtml, 'html'))
    messageA.attach(MIMEText(msgPlain, 'plain'))
    messageA.attach(messageR)

    message.attach(messageA)

    print("create_message_with_attachment: file: %s" % attachmentFile)
    content_type, encoding = mimetypes.guess_type(attachmentFile)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(attachmentFile)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    email.encoders.encode_base64(msg)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def main(unused_addr, to_email, mobile_num):
    to = to_email
    sender = "sjd.9f8.auy@gmail.com"
    subject = "Story for you"
    msgHtml = "I’ve been reading your stuff and think you’re the right reporter for this. I can’t tell you my \
    name (yet!). All I will say for now is that I work at Elektros as an engineer and have learned \
the company has been covering up a potentially deadly auto defect. \
<br><br>I can’t afford to quit (I have a family) but in good conscience I can’t allow the company to \
continue to profit while putting people’s lives at risk. The public (and the government!) has \
a right to know. \
<br><br>I’ve attached an interoffice message chain below. Read it. If you think this is a story you want \
to pursue, I can help. Reply ‘yes’ to this email and include your mobile phone number. I will \
then contact you."
    msgPlain = "I’ve been reading your stuff and think you’re the right reporter for this. I can’t tell you my \
    name (yet!). All I will say for now is that I work at Elektros as an engineer and have learned \
the company has been covering up a potentially deadly auto defect. \
\n\nI can’t afford to quit (I have a family) but in good conscience I can’t allow the company to\
continue to profit while putting people’s lives at risk. The public (and the government!) has \
a right to know. \
\n\nI’ve attached an interoffice message chain below. Read it. If you think this is a story you want \
to pursue, I can help. Reply ‘yes’ to this email and include your mobile phone number. I will \
then contact you."
   
    # send message without attachment
    # SendMessage(sender, to, subject, msgHtml, msgPlain)
   
    # Send message with attachment: 
    SendMessage(sender, to, subject, msgHtml, msgPlain, 'InterofficeCorrespondence.pdf')
    
    # get latest senders from our email
    no_match = True
    creds = get_credentials()
    while no_match:
        no_match = receive_emails.main(to, creds)
        time.sleep(10)

    subject = ""
    msgHtml = "Check Signal for further instructions."
    msgPlain = "Check Signal for further instructions."
    SendMessage(sender, to, subject, msgHtml, msgPlain)

    origWD = os.getcwd() # remember our original working directory
    # change directory to where signal-bat is installed
    os.chdir(os.path.join(origWD, "signal-cli/build/install/signal-cli/bin"))

    # text user via signal
    signal_receiver = "+" + mobile_num
    subprocess.run(["signal-cli.bat", "-u", "+16503088054", "send", \
        "-m", "We’re using Signal because it is more secure than email and \
other communication methods. Before we go further, let’s talk \
about the terms of my cooperation, i.e. what you reporters call \
a “source deal.” My name must not appear anywhere in any \
article, and you must promise to regard me as a confidential \
source. I will provide information “on guidance” and give you \
documents and other resources to support what I am telling you. \
To accept this deal, reply with ‘yes’.", signal_receiver])

    # wait for receiving message
    still_waiting = True  
    while still_waiting: 
        result = subprocess.run(["signal-cli.bat", "-u", "+16503088054", "receive"], stdout=subprocess.PIPE, errors='ignore', encoding='utf-8').stdout   

        numbers = [word for word in result.split() if word.startswith('+')]
        if numbers != [] and numbers[0][1:] == mobile_num:
            still_waiting = False
            print("found it!")
        else: 
            time.sleep(10)

    # send second signal text with audio attachment
    subprocess.run(["signal-cli.bat", "-u", "+16503088054", "send", \
        "-m", "", signal_receiver, "-a", "Recording.m4a"])

    os.chdir(origWD) # get back to our original working directory
    print("about to close server")
    server.shutdown()
    print("about to quit()")
    quit()
    

## TODO: needs to run automactically

if __name__ == '__main__':
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/email", main)
    server = osc_server.ThreadingOSCUDPServer(('127.0.0.1', 12345), dispatcher)
    print(server)
    server.serve_forever()
