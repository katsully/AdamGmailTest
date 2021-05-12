from googleapiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import file, client, tools
import os

import settings

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Gmail API Email'

def main(sender, credentials):
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=credentials.authorize(Http()))

    results = service.users().messages().list(userId='sjd.9f8.auy@gmail.com',labelIds = ['INBOX', 'UNREAD'], maxResults=5).execute()
    messages = results.get('messages', [])
    for message in messages:
            headers = service.users().messages().get(userId='sjd.9f8.auy@gmail.com', id=message['id']).execute()            
            msg_headers = headers['payload']['headers']
            for k in range(len(msg_headers)):       
                if msg_headers[k]['name'] == 'Return-Path':
                    new_sender = msg_headers[k]['value']
                    if "<"+sender+">" == new_sender:
                        return False
            return True

if __name__ == '__main__':
    main()

