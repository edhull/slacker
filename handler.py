import os
import re
import yaml
import base64
import binascii
import slack
import slack.chat
from aiosmtpd.handlers import Message


class MessageHandler(Message):
    def __init__(self, *args, **kargs):
        Message.__init__(self, *args, **kargs)

        config = os.getenv('CONFIG', '/etc/slacker/config.yml')
        print(config)
        if not os.path.exists(config):
            print('Config doesn\'t exists!')
            exit(1)

        self.config = yaml.load(open(config))


    def handle_message(self, message):
        """ This method will be called by aiosmtpd server when new mail will
            arrived.
        """
        options = self.process_rules(message)

        print('matched', options)
        self.send_to_slack(MessageHandler.decode_base64_if_required(message.get_payload()), **options)

        if options['debug']:
            self.send_to_slack('DEBUG: ' + str(message), **options)
              
    def decode_base64_if_required(input):
        """ Check if email follows SMTP/MIME base64 standard, and if so
            decode into string text
        """
        try:
            decoded = base64.b64decode(str(input)).decode('utf-8')
            return decoded
        except binascii.Error:
            return str(input)
        except UnicodeDecodeError:
            return str(input)
            

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
