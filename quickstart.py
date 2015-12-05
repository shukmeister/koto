from __future__ import print_function
import httplib2
import os

import base64
import email

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

"""Get history from 'sinceHistoryId' to present.
"""

def ListHistory(service, user_id, start_history_id='1'):
    """List History of all changes to the user's mailbox.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    start_history_id: Only return Histories at or after start_history_id.

    Returns:
    A list of mailbox changes that occurred after the start_history_id.
    """
    try:
        history = service.users().history().list(userId=user_id, startHistoryId=start_history_id).execute() 
        # changes = history['history'] if 'history' in history else []
        # while 'nextPageToken' in history:
        #     page_token = history['nextPageToken']
        #     history = (service.users().history().list(userId=user_id, startHistoryId=start_history_id, pageToken=page_token).execute())
        #     changes.extend(history['history'])
        # return changes
    except errors.HttpError, error:
        print("An error occurred: %s" % error)

def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format="full").execute()

    print ('Message snippet: %s' % message['snippet'])
    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

def GetMimeMessage(service, user_id, msg_id):
    """Get a Message and use it to create a MIME Message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

    Returns:
    A MIME Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()

        print ('Message snippet: %s' % message['snippet'])

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        mime_msg = email.message_from_string(msg_str)

        # mime_msg.as_string()
        # str(mime_msg)
        # repr(mime_msg)

        return mime_msg
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def GetThread(service, user_id, thread_id):
    """Get a Thread.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    thread_id: The ID of the Thread required.

    Returns:
    Thread with matching ID.
    """
    try:
        thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
        messages = thread['messages']
        print ('thread id: %s - number of messages in this thread: %d') % (thread['id'], len(messages))
        return thread
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # ListHistory(service, 'me')

    msgs = ListMessagesMatchingQuery(service, "me", "Ross")

    # for x in range (25, 30):
    #     print(msgs[x]['id'])
    #     print(GetMessage(service, "me", msgs[x]['id'])['parts'])


    print(msgs[30]['id'])
    encryptedMsg = GetMessage(service, "me", msgs[15]['id'])['payload']['parts'][1]['body']['data']
    deencryptedMsg = base64.urlsafe_b64decode(encryptedMsg.encode('UTF-8'))
    print(dehtml(deencryptedMsg))

    # print (GetThread(service, "me", msgs[0]['id']))

    # print (GetMimeMessage(service, "me", msgs[0]['id']))

    # if not msgs:
    #     print('no msgs found.')
    # else:
    #     print('Messages:')
    #     for x in msgs:
    #         msg = GetMessage(service, "me", x['id'])
    #         print(msg)

    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    #   for label in labels:
    #     print(label['name'])


if __name__ == '__main__':
    main()