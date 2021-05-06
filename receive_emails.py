from googleapiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import file, client, tools
import os

import settings

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Gmail API Email'

def main(sender):
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=credentials.authorize(Http()))

    results = service.users().messages().list(userId='me',labelIds = ['INBOX', 'UNREAD'], maxResults=5).execute()
    messages = results.get('messages', [])
    for message in messages:
            headers = service.users().messages().get(userId='me', id=message['id']).execute()            
            # print([a['value'] for a in headers['payload']['headers'] if a['name']=='From'][0])
            # for h in headers:
                # print(h)
            # print(headers['payload']['headers'])
            msg_headers = headers['payload']['headers']
            for k in range(len(msg_headers)):       
                if msg_headers[k]['name'] == 'Return-Path':
                    new_sender = msg_headers[k]['value']
                    print(sender)
                    print(new_sender)
                    if "<"+sender+">" == new_sender:
                        return False
            return True
            # test_sender = message["payload"]
            # print(headers['Return-Path'])
            # msg = service.users().messages().get(userId='me', id=message['id']).execute()
            # print(msg['snippet'])
            # Query the service object to get User Profile
            # userInfo = service.users().getProfile(userId='me').execute()
            # print("UserInfo is \n %s" % (userInfo))

if __name__ == '__main__':
    main()

