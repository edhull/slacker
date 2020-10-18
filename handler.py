import os
import re
import yaml
import base64
import binascii
import slack
import slack.chat
import html2text
import email
import requests
from aiosmtpd.handlers import Message
from hashlib import sha256
from base64 import b64encode, b64decode

class MessageHandler(Message):
    def __init__(self, *args, **kargs):
        Message.__init__(self, *args, **kargs)

        config = os.getenv('CONFIG', '/etc/slacker/config.yml')
        print(config)
        if not os.path.exists(config):
            print('Config doesn\'t exists!')
            exit(1)

        self.config = yaml.load(open(config))

    def email2text(data):
        body = email.message_from_bytes(data).get_payload()
        h = html2text.HTML2Text()
        h.ignore_tables = True
        return re.sub(r'\n\s*\n', '\n\n', h.handle(body))

    def handle_message(self, message):
        """ This method will be called by aiosmtpd server when new mail will
            arrive.
        """
        options = self.process_rules(message)
        print('matched', options)

        parsedMessage = email.message_from_string(message.as_string())
        
        body = ""

        if parsedMessage.is_multipart():
            for part in parsedMessage.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
                if ctype == 'text/html' and 'attachment' not in cdispo:
                    body = MessageHandler.email2text(part.get_payload(decode=True))  # decode
                    break
        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
        else:
            body = parsedMessage.get_payload(decode=True)
        
        if options['debug']:
            print(body)
            self.send_to_slack('DEBUG: ' + str(body), **options)

        self.send_to_slack(body, **options)

    def process_rules(self, message):
        """ Check every rule from config and returns options from matched
        """
        default = self.config['default']
        fields = {
            'from': message['From'],
            'to': message['To'],
            'subject': message['Subject'],
            'body': message.get_payload()
        }

        print(fields)

        for rule in self.config['rules']:
            tests = (re.match(rule[field], value) for field, value in fields.items() if field in rule)

            if all(tests):
                options = default.copy()
                options.update(rule['options'])
                return options

        return default


    def send_to_slack(self, text, **options):
        print('sending to slack', text, options)

        slack.api_token = options['slack_token']
        slack.chat.post_message(
            options['channel'],
            text,
            username=options['username'],
            icon_url=options['icon_url']
        )
